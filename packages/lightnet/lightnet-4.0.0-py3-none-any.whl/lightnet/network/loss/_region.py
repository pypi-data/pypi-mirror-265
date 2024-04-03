#
#   Darknet RegionLoss
#   Copyright EAVISE
#
import logging
import pandas as pd
import torch
from lightnet.util import iou_cwh, iou_wh
from lightnet._compat import meshgrid_kw
from ._base import Loss, MultiScale

__all__ = ['RegionLoss', 'MultiScaleRegionLoss']
log = logging.getLogger(__name__)


class RegionLoss(Loss):
    """
    Computes the region loss for anchor detection networks. |br|
    This loss is is meant to be used on the output of a :class:`~lightnet.network.head.DetectionAnchor` module,
    together with a brambox dataframe of target annotations.

    Args:
        num_classes (int): number of classes to detect
        anchors (ln.util.Anchors): single-scale list of anchor boxes
        network_stride (int): Downsampling factors of the network (most lightnet networks have a `stride` attribute)
        seen (optional, torch.Tensor): How many images the network has already been trained on; Default **0**
        coord_scale (optional, float): weight of bounding box coordinates; Default **1.0**
        noobject_scale (optional, float): weight of regions without target boxes; Default **1.0**
        object_scale (optional, float): weight of regions with target boxes; Default **5.0**
        class_scale (optional, float): weight of categorical predictions; Default **1.0**
        iou_thresh (optional, float): minimum iou between a predicted box and ground truth for them to be considered matching; Default **0.6**
        coord_prefill (optional, int): This parameter controls for how many training samples the network will prefill the target coordinates, biassing the network to predict the center at **.5,.5**; Default **12800**
        class_smoothing (optional, float): TODO
        coord_regression (optional, 'mse' | 'ciou'): TODO
        coord_grid_offset (optional, float): TODO
    """
    VALUES = ('total', 'conf', 'coord', 'class')
    ENABLE_REDUCTION = True

    def __init__(
        self,
        num_classes,
        anchors,
        network_stride,
        *,
        seen=0,
        iou_ignore_thresh=0.6,
        iou_merge_thresh=1,
        coord_scale=1.0,
        coord_regression='mse',
        coord_grid_sensitivity=1,
        coord_prefill=0,
        object_scale=5.0,
        noobject_scale=1.0,
        class_scale=1.0,
        class_smoothing=0,
        iou_thresh=None,    # Deprecated
    ):
        super().__init__()
        self.num_classes = num_classes
        self.num_anchors = anchors.num_anchors
        self.anchors = anchors.as_output(network_stride)
        self.network_stride = network_stride
        self.register_buffer('seen', torch.tensor(seen))

        self.iou_ignore_thresh = iou_ignore_thresh
        self.iou_merge_thresh = iou_merge_thresh
        self.coord_scale = coord_scale
        self.coord_regression = coord_regression.lower()
        self.coord_grid_sensitivity = coord_grid_sensitivity
        self.coord_prefill = coord_prefill
        self.object_scale = object_scale
        self.noobject_scale = noobject_scale
        self.class_scale = class_scale
        self.class_smoothing = class_smoothing

        assert self.coord_regression in ('mse', 'ciou'), 'The `coord_regression` parameter should be mse or ciou'
        if self.coord_regression == 'ciou' and self.coord_prefill > 0:
            log.warn('It is not recommended to use `coord_prefill` together with the CIoU regression method')

        if iou_thresh is not None:
            import warnings
            warnings.warn(
                'The `iou_thresh` argument is deprecated for the `iou_ignore_thresh`',
                category=DeprecationWarning,
                stacklevel=2,
            )
            self.iou_ignore_thresh = iou_thresh

    @property
    def loss(self):
        """
        .. deprecated:: 2.0.0
            |br| This "loss" attribute is deprecated in favor for "loss_total".
        """
        import warnings
        warnings.warn(
            'The "loss" attribute is deprecated in favor for "loss_total"',
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.loss_total

    def extra_repr(self):
        # TODO: Rework with new parameters
        anchors = ' '.join(f'[{a[0]:.5g}, {a[1]:.5g}]' for a in self.anchors)
        return (
            f'classes={self.num_classes}, network_stride={self.network_stride}, IoU threshold={self.iou_ignore_thresh}, seen={self.seen.item()}\n'
            f'coord_scale={self.coord_scale}, object_scale={self.object_scale}, noobject_scale={self.noobject_scale}, class_scale={self.class_scale}\n'
            f'anchors={anchors}'
        )

    def forward(self, output, target, *, seen=None):
        """
        Compute Region loss.

        Args:
            output (torch.autograd.Variable): Output from the network
            target (brambox annotation dataframe or torch.Tensor): Brambox annotations or tensor containing the annotation targets.
            seen (int, optional): How many images the network has already been trained on; Default **Add batch_size to previous seen value**

        Note:
            If using a target tensor, it should have the dimensions `[num_batch, num_anno, 5]`
            and have its coordinates relative to the image size (x divided by width, y divided by height).
            Since the annotations from all images of a batch should be made of the same length, you can pad them with: `[-1, 0, 0, 0, 0]`.

            More specifically, this is what the tensor should look like for one image:

            .. math::

                \\begin{bmatrix}
                    class\\_idx & x\\_center & y\\_center & width & height \\\\
                    class\\_idx & x\\_center & y\\_center & width & height \\\\
                    ... \\\\
                    -1 & 0 & 0 & 0 & 0 \\\\
                    -1 & 0 & 0 & 0 & 0 \\\\
                    ...
                \\end{bmatrix}

        Note:
            Besides being easier to work with, brambox dataframes have the added benefit that
            this loss function will also consider the ``ignore`` flag of annotations and ignore detections that match with it.
            This allows you to have annotations that will not influence the loss in any way,
            as opposed to having them removed and counting them as false detections.
        """
        # Parameters
        nA = self.num_anchors
        nC = self.num_classes
        nB, _, nH, nW = output.shape
        nPixels = nH * nW
        device = output.device
        if seen is not None:
            self.seen = torch.tensor(seen)
        elif self.training:
            self.seen += nB

        # Get x,y,w,h,conf,cls
        output = output.view(nB, nA, -1, nPixels)
        coord = torch.empty_like(output[:, :, :4])
        coord[:, :, :2] = self.coord_grid_sensitivity * output[:, :, :2].sigmoid() - 0.5 * (self.coord_grid_sensitivity - 1)    # tx,ty
        coord[:, :, 2:4] = output[:, :, 2:4]                                                                                    # tw,th
        conf = output[:, :, 4].sigmoid()
        if nC > 1:
            cls = output[:, :, 5:].transpose(-1, -2).reshape(-1, nC)

        with torch.no_grad():
            # Create prediction boxes
            pred_boxes = torch.FloatTensor(nB*nA*nPixels, 4)

            lin_y, lin_x = torch.meshgrid(torch.arange(nH), torch.arange(nW), **meshgrid_kw)
            lin_x = lin_x.reshape(-1).to(device)
            lin_y = lin_y.reshape(-1).to(device)
            anchor_w = self.anchors[:, 0].contiguous().view(nA, 1).to(device)
            anchor_h = self.anchors[:, 1].contiguous().view(nA, 1).to(device)

            # Compute max possible width/height network output, before the computed width/height would reach inf
            max_value = torch.tensor(1e35, dtype=pred_boxes.dtype, device=pred_boxes.device)
            max_w = (max_value / anchor_w.max()).log().floor()
            max_h = (max_value / anchor_h.max()).log().floor()

            # Get prediction coordinates
            pred_boxes[:, 0] = (coord[:, :, 0].detach() + lin_x).view(-1)
            pred_boxes[:, 1] = (coord[:, :, 1].detach() + lin_y).view(-1)
            pred_boxes[:, 2] = (coord[:, :, 2].detach().clamp(max=max_w).exp() * anchor_w).view(-1)
            pred_boxes[:, 3] = (coord[:, :, 3].detach().clamp(max=max_h).exp() * anchor_h).view(-1)
            pred_boxes = pred_boxes.cpu()

            # Get target values
            coord_mask, conf_mask, cls_mask, tcoord, tconf, tcls = self.build_targets(pred_boxes, target, nB, nH, nW)
            coord_mask = coord_mask.to(device).sqrt()
            conf_mask = conf_mask.to(device).sqrt()
            tcoord = tcoord.to(device)
            tconf = tconf.to(device)
            if nC > 1:
                tcls[~cls_mask] = -100                  # -100: ignored index CEL
                tcls = tcls.view(-1).long().to(device)

        # Confidence loss
        if self.object_scale == 0 and self.noobject_scale == 0:
            self.loss_conf = torch.tensor([0.0] * nB, device=device)
        else:
            self.loss_conf = torch.nn.functional.mse_loss(conf*conf_mask, tconf*conf_mask, reduction='none')
            self.loss_conf = self.loss_conf.sum(dim=tuple(range(1, self.loss_conf.ndim))) / 2

        # Coordinate loss
        if self.coord_scale == 0:
            self.loss_coord = torch.tensor([0.0] * nB, device=device)
        elif self.coord_regression == 'ciou':
            coord[:, :, 2] = coord[:, :, 2].clone().clamp(max=max_w).exp() * anchor_w
            coord[:, :, 3] = coord[:, :, 3].clone().clamp(max=max_h).exp() * anchor_h

            coord = coord.transpose(-1, -2)
            tcoord = tcoord.transpose(-1, -2)
            coord_mask = coord_mask.transpose(-1, -2)

            ciou = torch.ones_like(coord_mask)
            coord_mask = coord_mask > 0
            coord_mask_exp = coord_mask.expand_as(coord)
            ciou[coord_mask] = iou_cwh(coord[coord_mask_exp].reshape(-1, 4), tcoord[coord_mask_exp].reshape(-1, 4), pairwise=True, type=iou_cwh.Types.CIoU).squeeze()

            self.loss_coord = self.coord_scale * (1 - ciou).sum(dim=tuple(range(1, ciou.ndim)))
        else:
            with torch.no_grad():
                coord_mask = coord_mask.expand_as(tcoord)
                coord_wh = tcoord[:, :, 2:4, :] / self.anchors[:, :2].reshape(1, nA, 2, 1).to(device)
                coord_wh[coord_wh > 0] = coord_wh[coord_wh > 0].log()
                tcoord[:, :, 2:4, :] = coord_wh

            self.loss_coord = torch.nn.functional.mse_loss(coord*coord_mask, tcoord*coord_mask, reduction='none')
            self.loss_coord = self.coord_scale * self.loss_coord.sum(dim=tuple(range(1, self.loss_coord.ndim))) / 2

        # Class loss
        if self.class_scale == 0 or nC == 1 or tcls.numel() == 0:
            self.loss_class = torch.tensor([0.0] * nB, device=device)
        else:
            self.loss_class = torch.nn.functional.cross_entropy(cls, tcls, reduction='none', ignore_index=-100, label_smoothing=self.class_smoothing)
            self.loss_class = self.loss_class.view(nB, -1)
            self.loss_class = self.class_scale * self.loss_class.sum(dim=tuple(range(1, self.loss_class.ndim)))

        # Total loss
        self.loss_total = self.loss_conf + self.loss_coord + self.loss_class
        return self.loss_total

    def build_targets(self, pred_boxes, ground_truth, nB, nH, nW):
        """ Compare prediction boxes and targets, convert targets to network output tensors """
        if torch.is_tensor(ground_truth):
            return self.__build_targets_tensor(pred_boxes, ground_truth, nB, nH, nW)
        elif pd is not None and isinstance(ground_truth, pd.DataFrame):
            return self.__build_targets_brambox(pred_boxes, ground_truth, nB, nH, nW)
        else:
            raise TypeError(f'Unkown ground truth format [{type(ground_truth)}]')

    def __build_targets_tensor(self, pred_boxes, ground_truth, nB, nH, nW):
        """ Compare prediction boxes and ground truths, convert ground truths to network output tensors """
        # TODO : Deprecate this ?
        # Parameters
        nA = self.num_anchors
        nAnchors = nA*nH*nW
        nPixels = nH*nW

        # Tensors
        coord_mask = torch.zeros(nB, nA, nH, nW, requires_grad=False)
        conf_mask = torch.ones(nB, nA, nH, nW, requires_grad=False) * self.noobject_scale
        cls_mask = torch.zeros(nB, nA, nH, nW, dtype=torch.bool, requires_grad=False)
        tcoord = torch.zeros(nB, nA, 4, nH, nW, requires_grad=False)
        tconf = torch.zeros(nB, nA, nH, nW, requires_grad=False)
        tcls = torch.zeros(nB, nA, nH, nW, requires_grad=False)

        if self.training and self.seen < self.coord_prefill:
            coord_mask.fill_((.01 / self.coord_scale) ** 0.5)
            tcoord[:, :, 0].fill_(0.5)
            tcoord[:, :, 1].fill_(0.5)

        # Loop over GT
        for b in range(nB):
            gt = ground_truth[b][(ground_truth[b, :, 0] >= 0)[:, None].expand_as(ground_truth[b])].view(-1, 5)
            if gt.numel() == 0:     # No gt for this image
                continue

            # Build up tensors
            cur_pred_boxes = pred_boxes[b*nAnchors:(b+1)*nAnchors]
            gt = gt[:, 1:]
            gt[:, ::2] *= nW
            gt[:, 1::2] *= nH

            # Set confidence mask of matching detections to 0
            iou_gt_pred = iou_cwh(gt, cur_pred_boxes)
            mask = (iou_gt_pred > self.iou_ignore_thresh).any(0)
            conf_mask[b][mask.view_as(conf_mask[b])] = 0

            # Find best anchor for each gt
            iou_gt_anchors = iou_wh(gt[:, 2:], self.anchors)
            _, best_anchors = iou_gt_anchors.max(1)

            # Set masks and target values for each gt
            nGT = gt.shape[0]
            gi = gt[:, 0].clamp(0, nW-1).long()
            gj = gt[:, 1].clamp(0, nH-1).long()

            conf_mask[b, best_anchors, gj, gi] = self.object_scale
            tconf[b, best_anchors, gj, gi] = iou_gt_pred.view(nGT, nA, nH, nW)[torch.arange(nGT), best_anchors, gj, gi]
            coord_mask[b, best_anchors, gj, gi] = 2 - torch.clamp(gt[:, 2] * gt[:, 3] / nPixels, max=1.5)
            tcoord[b, best_anchors, 0, gj, gi] = gt[:, 0] - gi.float()
            tcoord[b, best_anchors, 1, gj, gi] = gt[:, 1] - gj.float()
            tcoord[b, best_anchors, 2:4, gj, gi] = gt[:, 2:4]
            cls_mask[b, best_anchors, gj, gi] = 1
            tcls[b, best_anchors, gj, gi] = ground_truth[b, torch.arange(nGT), 0]

        return (
            coord_mask.view(nB, nA, 1, nPixels),
            conf_mask.view(nB, nA, nPixels),
            cls_mask.view(nB, nA, nPixels),
            tcoord.view(nB, nA, 4, nPixels),
            tconf.view(nB, nA, nPixels),
            tcls.view(nB, nA, nPixels),
        )

    def __build_targets_brambox(self, pred_boxes, ground_truth, nB, nH, nW):
        """ Compare prediction boxes and ground truths, convert ground truths to network output tensors """
        # Parameters
        nA = self.num_anchors
        nAnchors = nA*nH*nW
        nPixels = nH*nW

        # Tensors
        coord_mask = torch.zeros(nB, nA, nH, nW)
        conf_mask = torch.ones(nB, nA, nH, nW) * self.noobject_scale
        cls_mask = torch.zeros(nB, nA, nH, nW, dtype=torch.bool)
        tcoord = torch.zeros(nB, nA, 4, nH, nW)
        tconf = torch.zeros(nB, nA, nH, nW)
        tcls = torch.zeros(nB, nA, nH, nW)

        if self.training and self.seen < self.coord_prefill:
            coord_mask.fill_((.01 / self.coord_scale) ** 0.5)
            tcoord[:, :, 0].fill_(0.5)
            tcoord[:, :, 1].fill_(0.5)

        # Loop over GT
        for b, gt_filtered in ground_truth.groupby('batch_number', sort=False):
            cur_pred_boxes = pred_boxes[b*nAnchors:(b+1)*nAnchors]

            # Create ground_truth tensor
            gt = torch.from_numpy(gt_filtered[['x_top_left', 'y_top_left', 'width', 'height']].to_numpy(copy=True)).float()
            nGT = gt.shape[0]

            # Convert from topleft -> center
            gt[:, 0] += gt[:, 2] / 2
            gt[:, 1] += gt[:, 3] / 2

            # Divide coordinates by stride
            gt[:, :4] /= self.network_stride

            # Get grid cell coordinate
            gi = gt[:, 0].clamp(0, nW-1).long()
            gj = gt[:, 1].clamp(0, nH-1).long()

            # Compute IoU between GT and predictions
            iou_gt_pred = iou_cwh(gt, cur_pred_boxes)

            # Set mask and target values for each matching detection (iou_merge_thresh)
            match_iou, match_gt = iou_gt_pred.max(0)
            mask = match_iou > self.iou_merge_thresh
            if gt_filtered.ignore.any():
                ignore_mask = torch.from_numpy(gt_filtered.ignore.values)
                mask &= torch.isin(match_gt, ignore_mask.nonzero(), invert=True)

            if mask.any():
                mask = mask.nonzero().flatten()
                anchor_match = mask // nPixels
                gi_match = (mask % nPixels) % nW
                gj_match = (mask % nPixels) // nW
                gt_match_idx = match_gt[mask]
                gt_match = gt[gt_match_idx]

                conf_mask[b, anchor_match, gj_match, gi_match] = 1
                tconf[b, anchor_match, gj_match, gi_match] = iou_gt_pred.view(nGT, nA, nH, nW)[gt_match_idx, anchor_match, gj_match, gi_match]
                coord_mask[b, anchor_match, gj_match, gi_match] = 2 - torch.clamp(gt_match[:, 2] * gt_match[:, 3] / nPixels, max=1.5)
                tcoord[b, anchor_match, 0, gj_match, gi_match] = gt_match[:, 0] - gi_match.float()
                tcoord[b, anchor_match, 1, gj_match, gi_match] = gt_match[:, 1] - gj_match.float()
                tcoord[b, anchor_match, 2:4, gj_match, gi_match] = gt_match[:, 2:4]
                cls_mask[b, anchor_match, gj_match, gi_match] = 1
                tcls[b, anchor_match, gj_match, gi_match] = torch.from_numpy(gt_filtered.class_id.values)[gt_match_idx].float()

            # Set masks of matching detections to 0 (iou_ignore_thresh)
            mask = (iou_gt_pred > self.iou_ignore_thresh).any(dim=0)
            mask = mask.view_as(conf_mask[b])
            conf_mask[b, mask] = 0
            # coord_mask[b, mask] = 0
            # cls_mask[b, mask] = 0

            # Find best anchor for each gt
            iou_gt_anchors = iou_wh(gt[:, 2:], self.anchors)
            _, best_anchors = iou_gt_anchors.max(1)

            # Set masks and target values for each best matching (anchor, gt) pair
            conf_mask[b, best_anchors, gj, gi] = self.object_scale
            tconf[b, best_anchors, gj, gi] = iou_gt_pred.view(nGT, nA, nH, nW)[torch.arange(nGT), best_anchors, gj, gi]
            coord_mask[b, best_anchors, gj, gi] = 2 - torch.clamp(gt[:, 2] * gt[:, 3] / nPixels, max=1.5)
            tcoord[b, best_anchors, 0, gj, gi] = gt[:, 0] - gi.float()
            tcoord[b, best_anchors, 1, gj, gi] = gt[:, 1] - gj.float()
            tcoord[b, best_anchors, 2:4, gj, gi] = gt[:, 2:4]
            cls_mask[b, best_anchors, gj, gi] = 1
            tcls[b, best_anchors, gj, gi] = torch.from_numpy(gt_filtered.class_id.values).float()

            # Set masks of ignored to zero
            if gt_filtered.ignore.any():
                ignore_mask = torch.from_numpy(gt_filtered.ignore.values)
                gi = gi[ignore_mask]
                gj = gj[ignore_mask]
                best_anchors = best_anchors[ignore_mask]

                conf_mask[b, best_anchors, gj, gi] = 0
                coord_mask[b, best_anchors, gj, gi] = 0
                cls_mask[b, best_anchors, gj, gi] = 0

        return (
            coord_mask.view(nB, nA, 1, nPixels),
            conf_mask.view(nB, nA, nPixels),
            cls_mask.view(nB, nA, nPixels),
            tcoord.view(nB, nA, 4, nPixels),
            tconf.view(nB, nA, nPixels),
            tcls.view(nB, nA, nPixels),
        )


class MultiScaleRegionLoss(MultiScale, RegionLoss):
    """
    Computes the region loss for multiscale anchor detection networks. |br|
    This class is is meant to be used on the output of multiple :class:`~lightnet.network.head.DetectionAnchor` modules,
    together with a brambox dataframe of target annotations.

    Args:
        num_classes (int): number of classes to detect
        anchors (ln.util.Anchors): multi-scale list of anchor boxes
        network_stride (list): Downsampling factors of the network (most lightnet networks have a `stride` attribute)
        seen (optional, torch.Tensor): How many images the network has already been trained on; Default **0**
        coord_scale (optional, float): weight of bounding box coordinates; Default **1.0**
        noobject_scale (optional, float): weight of regions without target boxes; Default **1.0**
        object_scale (optional, float): weight of regions with target boxes; Default **5.0**
        class_scale (optional, float): weight of categorical predictions; Default **1.0**
        iou_thresh (optional, float): minimum iou between a predicted box and ground truth for them to be considered matching; Default **0.6**
        coord_prefill (optional, int): This parameter controls for how many training samples the network will prefill the target coordinates, biassing the network to predict the center at **.5,.5**; Default **12800**

    Note:
        All parameters are the same as :class:`~lightnet.network.loss.RegionLoss`, except for `anchors` and `network_stride`. |br|
        These 2 parameters need separate values for each different network output scale and thus need to be lists of the original parameter.

    Warning:
        This loss function is not entirely equivalent to the Darknet implementation! |br|
        We just execute the regular :class:`~lightnet.network.loss.RegionLoss` at multiple scales (different strides and anchors),
        and as such did not implement overlapping class labels.
    """
    LOSS = RegionLoss
    MULTISCALE_ARGS = ('anchors', 'network_stride')

    @staticmethod
    def _setup_multiscale_args(ms_args):
        """ Keep only scale specific anchors. """
        ms_args['anchors'] = ms_args['anchors'].split_scales()
        return MultiScale._setup_multiscale_args(ms_args)

    def _postprocess_multiscale_arg(self, ms_args, idx):
        """ Transform anchors to output relative tensors. """
        ms_args['num_anchors'] = ms_args['anchors'].num_anchors
        ms_args['anchors'] = ms_args['anchors'].as_output(ms_args['network_stride'])
        return ms_args

    def _setup_forward_kwargs(self, output, target, kwargs):
        """ Setup seen argument because otherwise each scale forward run will increase its value. """
        if 'seen' not in kwargs:
            kwargs['seen'] = self.seen.item() + output[0].shape[0]
        return kwargs

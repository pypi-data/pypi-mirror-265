#
#   Darknet YOLOv4 model
#   Copyright EAVISE
#
import functools
import torch.nn as nn
import lightnet as ln
import lightnet.network as lnn

__all__ = ['YoloV4']


class YoloV4(lnn.module.Darknet):
    """ Yolo v4 implementation :cite:`yolo_v4`.

    Args:
        num_classes (int): Number of classes
        input_channels (int, optional): Number of input channels; Default **3**
        anchors (ln.util.Anchors, optional): single-scale list of anchor boxes; Default **Darknet YoloV3 COCO**

    Attributes:
        self.stride: Subsampling factors of the network (input_dim / output_dim)
        self.inner_stride: Maximal internal subsampling factor of the network (input dimension should be a multiple of this)
        self.remap_cspdarknet53: Remapping rules for weights from the :class:`~lightnet.models.CSPDarknet53` model.
        self.remap_tianxiaomo: Remapping rules for weights from the `pytorch-YOLOv4 <https://github.com/Tianxiaomo/pytorch-YOLOv4>`_ repository.

    Note:
        The preferred way to pass anchors is to use the :class:`~lightnet.util.Anchors`.
        However, for compatibility reasons, you can also pass in a list of tuples,
        which will be interpreted as darknet anchors (relative to input dimensions).
    """
    stride = (32, 16, 8)
    inner_stride = 32
    values_per_anchor = 2

    remap_cspdarknet53 = (
        (r'^backbone\.(.*)', r'backbone.module.\1'),
    )

    # https://github.com/Tianxiaomo/pytorch-YOLOv4
    remap_tianxiaomo = (
        (r'down1.conv1.conv\.(.*)', r'backbone.module.1_convbatch.layers.\1'),
        (r'down1.conv2.conv\.(.*)', r'backbone.module.2_convbatch.layers.\1'),
        (r'down1.conv3.conv\.(.*)', r'backbone.module.3_csp.split1.layers.\1'),
        (r'down1.conv4.conv\.(.*)', r'backbone.module.3_csp.split2.layers.\1'),
        (r'down1.conv5.conv\.(.*)', r'backbone.module.3_csp.residual1.0.layers.\1'),
        (r'down1.conv6.conv\.(.*)', r'backbone.module.3_csp.residual1.1.layers.\1'),
        (r'down1.conv7.conv\.(.*)', r'backbone.module.3_csp.conv.layers.\1'),
        (r'down1.conv8.conv\.(.*)', r'backbone.module.3_csp.post.layers.\1'),
        (r'down2.conv1.conv\.(.*)', r'backbone.module.4_convbatch.layers.\1'),
        (r'down2.conv2.conv\.(.*)', r'backbone.module.5_csp.split1.layers.\1'),
        (r'down2.conv3.conv\.(.*)', r'backbone.module.5_csp.split2.layers.\1'),
        (r'down2.conv4.conv\.(.*)', r'backbone.module.5_csp.conv.layers.\1'),
        (r'down2.conv5.conv\.(.*)', r'backbone.module.5_csp.post.layers.\1'),
        (r'down2.resblock.module_list.0.0.conv\.(.*)', r'backbone.module.5_csp.residual1.0.layers.\1'),
        (r'down2.resblock.module_list.0.1.conv\.(.*)', r'backbone.module.5_csp.residual1.1.layers.\1'),
        (r'down2.resblock.module_list.1.0.conv\.(.*)', r'backbone.module.5_csp.residual2.0.layers.\1'),
        (r'down2.resblock.module_list.1.1.conv\.(.*)', r'backbone.module.5_csp.residual2.1.layers.\1'),
        (r'down3.conv1.conv\.(.*)', r'backbone.module.6_convbatch.layers.\1'),
        (r'down3.conv2.conv\.(.*)', r'backbone.module.7_csp.split1.layers.\1'),
        (r'down3.conv3.conv\.(.*)', r'backbone.module.7_csp.split2.layers.\1'),
        (r'down3.conv4.conv\.(.*)', r'backbone.module.7_csp.conv.layers.\1'),
        (r'down3.conv5.conv\.(.*)', r'backbone.module.7_csp.post.layers.\1'),
        (r'down3.resblock.module_list.0.0.conv\.(.*)', r'backbone.module.7_csp.residual1.0.layers.\1'),
        (r'down3.resblock.module_list.0.1.conv\.(.*)', r'backbone.module.7_csp.residual1.1.layers.\1'),
        (r'down3.resblock.module_list.1.0.conv\.(.*)', r'backbone.module.7_csp.residual2.0.layers.\1'),
        (r'down3.resblock.module_list.1.1.conv\.(.*)', r'backbone.module.7_csp.residual2.1.layers.\1'),
        (r'down3.resblock.module_list.2.0.conv\.(.*)', r'backbone.module.7_csp.residual3.0.layers.\1'),
        (r'down3.resblock.module_list.2.1.conv\.(.*)', r'backbone.module.7_csp.residual3.1.layers.\1'),
        (r'down3.resblock.module_list.3.0.conv\.(.*)', r'backbone.module.7_csp.residual4.0.layers.\1'),
        (r'down3.resblock.module_list.3.1.conv\.(.*)', r'backbone.module.7_csp.residual4.1.layers.\1'),
        (r'down3.resblock.module_list.4.0.conv\.(.*)', r'backbone.module.7_csp.residual5.0.layers.\1'),
        (r'down3.resblock.module_list.4.1.conv\.(.*)', r'backbone.module.7_csp.residual5.1.layers.\1'),
        (r'down3.resblock.module_list.5.0.conv\.(.*)', r'backbone.module.7_csp.residual6.0.layers.\1'),
        (r'down3.resblock.module_list.5.1.conv\.(.*)', r'backbone.module.7_csp.residual6.1.layers.\1'),
        (r'down3.resblock.module_list.6.0.conv\.(.*)', r'backbone.module.7_csp.residual7.0.layers.\1'),
        (r'down3.resblock.module_list.6.1.conv\.(.*)', r'backbone.module.7_csp.residual7.1.layers.\1'),
        (r'down3.resblock.module_list.7.0.conv\.(.*)', r'backbone.module.7_csp.residual8.0.layers.\1'),
        (r'down3.resblock.module_list.7.1.conv\.(.*)', r'backbone.module.7_csp.residual8.1.layers.\1'),
        (r'down4.conv1.conv\.(.*)', r'backbone.module.8_convbatch.layers.\1'),
        (r'down4.conv2.conv\.(.*)', r'backbone.module.9_csp.split1.layers.\1'),
        (r'down4.conv3.conv\.(.*)', r'backbone.module.9_csp.split2.layers.\1'),
        (r'down4.conv4.conv\.(.*)', r'backbone.module.9_csp.conv.layers.\1'),
        (r'down4.conv5.conv\.(.*)', r'backbone.module.9_csp.post.layers.\1'),
        (r'down4.resblock.module_list.0.0.conv\.(.*)', r'backbone.module.9_csp.residual1.0.layers.\1'),
        (r'down4.resblock.module_list.0.1.conv\.(.*)', r'backbone.module.9_csp.residual1.1.layers.\1'),
        (r'down4.resblock.module_list.1.0.conv\.(.*)', r'backbone.module.9_csp.residual2.0.layers.\1'),
        (r'down4.resblock.module_list.1.1.conv\.(.*)', r'backbone.module.9_csp.residual2.1.layers.\1'),
        (r'down4.resblock.module_list.2.0.conv\.(.*)', r'backbone.module.9_csp.residual3.0.layers.\1'),
        (r'down4.resblock.module_list.2.1.conv\.(.*)', r'backbone.module.9_csp.residual3.1.layers.\1'),
        (r'down4.resblock.module_list.3.0.conv\.(.*)', r'backbone.module.9_csp.residual4.0.layers.\1'),
        (r'down4.resblock.module_list.3.1.conv\.(.*)', r'backbone.module.9_csp.residual4.1.layers.\1'),
        (r'down4.resblock.module_list.4.0.conv\.(.*)', r'backbone.module.9_csp.residual5.0.layers.\1'),
        (r'down4.resblock.module_list.4.1.conv\.(.*)', r'backbone.module.9_csp.residual5.1.layers.\1'),
        (r'down4.resblock.module_list.5.0.conv\.(.*)', r'backbone.module.9_csp.residual6.0.layers.\1'),
        (r'down4.resblock.module_list.5.1.conv\.(.*)', r'backbone.module.9_csp.residual6.1.layers.\1'),
        (r'down4.resblock.module_list.6.0.conv\.(.*)', r'backbone.module.9_csp.residual7.0.layers.\1'),
        (r'down4.resblock.module_list.6.1.conv\.(.*)', r'backbone.module.9_csp.residual7.1.layers.\1'),
        (r'down4.resblock.module_list.7.0.conv\.(.*)', r'backbone.module.9_csp.residual8.0.layers.\1'),
        (r'down4.resblock.module_list.7.1.conv\.(.*)', r'backbone.module.9_csp.residual8.1.layers.\1'),
        (r'down5.conv1.conv\.(.*)', r'backbone.module.10_convbatch.layers.\1'),
        (r'down5.conv2.conv\.(.*)', r'backbone.module.11_csp.split1.layers.\1'),
        (r'down5.conv3.conv\.(.*)', r'backbone.module.11_csp.split2.layers.\1'),
        (r'down5.conv4.conv\.(.*)', r'backbone.module.11_csp.conv.layers.\1'),
        (r'down5.conv5.conv\.(.*)', r'backbone.module.11_csp.post.layers.\1'),
        (r'down5.resblock.module_list.0.0.conv\.(.*)', r'backbone.module.11_csp.residual1.0.layers.\1'),
        (r'down5.resblock.module_list.0.1.conv\.(.*)', r'backbone.module.11_csp.residual1.1.layers.\1'),
        (r'down5.resblock.module_list.1.0.conv\.(.*)', r'backbone.module.11_csp.residual2.0.layers.\1'),
        (r'down5.resblock.module_list.1.1.conv\.(.*)', r'backbone.module.11_csp.residual2.1.layers.\1'),
        (r'down5.resblock.module_list.2.0.conv\.(.*)', r'backbone.module.11_csp.residual3.0.layers.\1'),
        (r'down5.resblock.module_list.2.1.conv\.(.*)', r'backbone.module.11_csp.residual3.1.layers.\1'),
        (r'down5.resblock.module_list.3.0.conv\.(.*)', r'backbone.module.11_csp.residual4.0.layers.\1'),
        (r'down5.resblock.module_list.3.1.conv\.(.*)', r'backbone.module.11_csp.residual4.1.layers.\1'),
        # Some weight files contain a misspelled "neek" instead of "neck"
        (r'ne[ec]k.conv1.conv\.(.*)', r'neck.0.0.layers.\1'),
        (r'ne[ec]k.conv10.conv\.(.*)', r'neck.1.combine.0.2.layers.\1'),
        (r'ne[ec]k.conv11.conv\.(.*)', r'neck.1.combine.0.3.layers.\1'),
        (r'ne[ec]k.conv12.conv\.(.*)', r'neck.1.combine.0.4.layers.\1'),
        (r'ne[ec]k.conv13.conv\.(.*)', r'neck.1.combine.0.5.layers.\1'),
        (r'ne[ec]k.conv14.conv\.(.*)', r'neck.1.upsample.1.0.layers.\1'),
        (r'ne[ec]k.conv15.conv\.(.*)', r'neck.1.lateral.2.layers.\1'),
        (r'ne[ec]k.conv16.conv\.(.*)', r'neck.1.combine.1.1.layers.\1'),
        (r'ne[ec]k.conv17.conv\.(.*)', r'neck.1.combine.1.2.layers.\1'),
        (r'ne[ec]k.conv18.conv\.(.*)', r'neck.1.combine.1.3.layers.\1'),
        (r'ne[ec]k.conv19.conv\.(.*)', r'neck.1.combine.1.4.layers.\1'),
        (r'ne[ec]k.conv2.conv\.(.*)', r'neck.0.1.layers.\1'),
        (r'ne[ec]k.conv20.conv\.(.*)', r'neck.1.combine.1.5.layers.\1'),
        (r'ne[ec]k.conv3.conv\.(.*)', r'neck.0.2.layers.\1'),
        (r'ne[ec]k.conv4.conv\.(.*)', r'neck.0.4.layers.\1'),
        (r'ne[ec]k.conv5.conv\.(.*)', r'neck.0.5.layers.\1'),
        (r'ne[ec]k.conv6.conv\.(.*)', r'neck.1.lateral.0.layers.\1'),
        (r'ne[ec]k.conv7.conv\.(.*)', r'neck.1.upsample.0.0.layers.\1'),
        (r'ne[ec]k.conv8.conv\.(.*)', r'neck.1.lateral.1.layers.\1'),
        (r'ne[ec]k.conv9.conv\.(.*)', r'neck.1.combine.0.1.layers.\1'),
        (r'head.conv1.conv\.(.*)', r'head.2.0.layers.\1'),
        (r'head.conv10.conv.0\.(.*)', r'head.1.1.\1'),
        (r'head.conv11.conv\.(.*)', r'neck.1.downsample.1.layers.\1'),
        (r'head.conv12.conv\.(.*)', r'neck.1.combine.3.1.layers.\1'),
        (r'head.conv13.conv\.(.*)', r'neck.1.combine.3.2.layers.\1'),
        (r'head.conv14.conv\.(.*)', r'neck.1.combine.3.3.layers.\1'),
        (r'head.conv15.conv\.(.*)', r'neck.1.combine.3.4.layers.\1'),
        (r'head.conv16.conv\.(.*)', r'neck.1.combine.3.5.layers.\1'),
        (r'head.conv17.conv\.(.*)', r'head.0.0.layers.\1'),
        (r'head.conv18.conv.0\.(.*)', r'head.0.1.\1'),
        (r'head.conv2.conv.0\.(.*)', r'head.2.1.\1'),
        (r'head.conv3.conv\.(.*)', r'neck.1.downsample.0.layers.\1'),
        (r'head.conv4.conv\.(.*)', r'neck.1.combine.2.1.layers.\1'),
        (r'head.conv5.conv\.(.*)', r'neck.1.combine.2.2.layers.\1'),
        (r'head.conv6.conv\.(.*)', r'neck.1.combine.2.3.layers.\1'),
        (r'head.conv7.conv\.(.*)', r'neck.1.combine.2.4.layers.\1'),
        (r'head.conv8.conv\.(.*)', r'neck.1.combine.2.5.layers.\1'),
        (r'head.conv9.conv\.(.*)', r'head.1.0.layers.\1'),
    )

    # Darknet weight file module order is different than our modeling (this gets automatically applied)
    darknet_order = (
        'backbone.module.1_convbatch',
        'backbone.module.2_convbatch',
        'backbone.module.3_csp.split2',
        'backbone.module.3_csp.split1',
        'backbone.module.3_csp.residual1.0',
        'backbone.module.3_csp.residual1.1',
        'backbone.module.3_csp.conv',
        'backbone.module.3_csp.post',
        'backbone.module.4_convbatch',
        'backbone.module.5_csp.split2',
        'backbone.module.5_csp.split1',
        'backbone.module.5_csp.residual1.0',
        'backbone.module.5_csp.residual1.1',
        'backbone.module.5_csp.residual2.0',
        'backbone.module.5_csp.residual2.1',
        'backbone.module.5_csp.conv',
        'backbone.module.5_csp.post',
        'backbone.module.6_convbatch',
        'backbone.module.7_csp.split2',
        'backbone.module.7_csp.split1',
        'backbone.module.7_csp.residual1.0',
        'backbone.module.7_csp.residual1.1',
        'backbone.module.7_csp.residual2.0',
        'backbone.module.7_csp.residual2.1',
        'backbone.module.7_csp.residual3.0',
        'backbone.module.7_csp.residual3.1',
        'backbone.module.7_csp.residual4.0',
        'backbone.module.7_csp.residual4.1',
        'backbone.module.7_csp.residual5.0',
        'backbone.module.7_csp.residual5.1',
        'backbone.module.7_csp.residual6.0',
        'backbone.module.7_csp.residual6.1',
        'backbone.module.7_csp.residual7.0',
        'backbone.module.7_csp.residual7.1',
        'backbone.module.7_csp.residual8.0',
        'backbone.module.7_csp.residual8.1',
        'backbone.module.7_csp.conv',
        'backbone.module.7_csp.post',
        'backbone.module.8_convbatch',
        'backbone.module.9_csp.split2',
        'backbone.module.9_csp.split1',
        'backbone.module.9_csp.residual1.0',
        'backbone.module.9_csp.residual1.1',
        'backbone.module.9_csp.residual2.0',
        'backbone.module.9_csp.residual2.1',
        'backbone.module.9_csp.residual3.0',
        'backbone.module.9_csp.residual3.1',
        'backbone.module.9_csp.residual4.0',
        'backbone.module.9_csp.residual4.1',
        'backbone.module.9_csp.residual5.0',
        'backbone.module.9_csp.residual5.1',
        'backbone.module.9_csp.residual6.0',
        'backbone.module.9_csp.residual6.1',
        'backbone.module.9_csp.residual7.0',
        'backbone.module.9_csp.residual7.1',
        'backbone.module.9_csp.residual8.0',
        'backbone.module.9_csp.residual8.1',
        'backbone.module.9_csp.conv',
        'backbone.module.9_csp.post',
        'backbone.module.10_convbatch',
        'backbone.module.11_csp.split2',
        'backbone.module.11_csp.split1',
        'backbone.module.11_csp.residual1.0',
        'backbone.module.11_csp.residual1.1',
        'backbone.module.11_csp.residual2.0',
        'backbone.module.11_csp.residual2.1',
        'backbone.module.11_csp.residual3.0',
        'backbone.module.11_csp.residual3.1',
        'backbone.module.11_csp.residual4.0',
        'backbone.module.11_csp.residual4.1',
        'backbone.module.11_csp.conv',
        'backbone.module.11_csp.post',
        'neck.0.0',
        'neck.0.1',
        'neck.0.2',
        'neck.0.4',
        'neck.0.5',
        'neck.1.lateral.0',
        'neck.1.upsample.0.0',
        'neck.1.lateral.1',
        'neck.1.combine.0.1',
        'neck.1.combine.0.2',
        'neck.1.combine.0.3',
        'neck.1.combine.0.4',
        'neck.1.combine.0.5',
        'neck.1.upsample.1.0',
        'neck.1.lateral.2',
        'neck.1.combine.1.1',
        'neck.1.combine.1.2',
        'neck.1.combine.1.3',
        'neck.1.combine.1.4',
        'neck.1.combine.1.5',
        'head.2.0',
        'head.2.1',
        'neck.1.downsample.0',
        'neck.1.combine.2.1',
        'neck.1.combine.2.2',
        'neck.1.combine.2.3',
        'neck.1.combine.2.4',
        'neck.1.combine.2.5',
        'head.1.0',
        'head.1.1',
        'neck.1.downsample.1',
        'neck.1.combine.3.1',
        'neck.1.combine.3.2',
        'neck.1.combine.3.3',
        'neck.1.combine.3.4',
        'neck.1.combine.3.5',
        'head.0.0',
        'head.0.1',
    )

    def __init_module__(
        self,
        num_classes,
        input_channels=3,
        outputs=(True, True, True),
        anchors=ln.util.Anchors.YoloV4_COCO,
    ):
        if len(outputs) != 3:
            raise ValueError('The `outputs` argument should be a list of 3 boolean values')
        if not any(outputs):
            raise ValueError('We need at least one output block')

        if not isinstance(anchors, ln.util.Anchors):
            anchors = ln.util.Anchors.from_darknet(self, anchors)
        if anchors.num_scales != sum(outputs):
            raise ln.util.AnchorError(anchors, f'Expected {sum(outputs)} scales, but got {anchors.num_scales}')
        if anchors.values_per_anchor != self.values_per_anchor:
            raise ln.util.AnchorError(anchors, f'Expected {self.values_per_anchor} values per anchor, but got {anchors.values_per_anchor}')

        self.num_classes = num_classes
        self.outputs = outputs
        self.anchors = anchors
        self.stride = tuple(s for s, o in zip(self.stride, self.outputs) if o)
        if sum(self.outputs) == 1:
            self.stride = self.stride[0]

        # Network
        activation_backbone = functools.partial(nn.Mish, inplace=True)
        activation_head = functools.partial(nn.LeakyReLU, 0.1, inplace=True)
        momentum = 0.051

        self.backbone = lnn.layer.FeatureExtractor(
            lnn.backbone.CSPDarknet53(input_channels, 1024, activation=activation_backbone, momentum=momentum),
            ['9_csp', '7_csp'],
            True,
        )

        self.neck = nn.ModuleList([
            # SPP (with extra convolutions around)
            nn.Sequential(
                lnn.layer.Conv2dBatchAct(1024, 512, 1, 1, 0, activation=activation_head, momentum=momentum),
                lnn.layer.Conv2dBatchAct(512, 1024, 3, 1, 1, activation=activation_head, momentum=momentum),
                lnn.layer.Conv2dBatchAct(1024, 512, 1, 1, 0, activation=activation_head, momentum=momentum),
                lnn.layer.ParallelCat(
                    nn.MaxPool2d(13, 1, 13 // 2),
                    nn.MaxPool2d(9, 1, 9 // 2),
                    nn.MaxPool2d(5, 1, 5 // 2),
                    nn.Identity(),
                ),
                lnn.layer.Conv2dBatchAct(2048, 512, 1, 1, 0, activation=activation_head, momentum=momentum),
                lnn.layer.Conv2dBatchAct(512, 1024, 3, 1, 1, activation=activation_head, momentum=momentum),
            ),

            # PANet
            lnn.layer.PAFPN(
                [1024, 512, 256],
                [512, 256, 128],

                make_lateral=lambda ci, co: lnn.layer.Conv2dBatchAct(ci, co, 1, 1, 0, activation=activation_head, momentum=momentum),

                make_upsample=lambda ci, co: nn.Sequential(
                    lnn.layer.Conv2dBatchAct(ci, co, 1, 1, 0, activation=activation_head, momentum=momentum),
                    nn.Upsample(scale_factor=2, mode='nearest'),
                ),

                make_downsample=lambda ci, co: lnn.layer.Conv2dBatchAct(ci, co, 3, 2, 1, activation=activation_head, momentum=momentum),

                # Note: ci should be equal to co
                make_combine=lambda ci, co: nn.Sequential(
                    lnn.layer.Combinator(type='cat'),
                    lnn.layer.Conv2dBatchAct(ci*2, co, 1, 1, 0, activation=activation_head, momentum=momentum),
                    lnn.layer.Conv2dBatchAct(co, co*2, 3, 1, 1, activation=activation_head, momentum=momentum),
                    lnn.layer.Conv2dBatchAct(co*2, co, 1, 1, 0, activation=activation_head, momentum=momentum),
                    lnn.layer.Conv2dBatchAct(co, co*2, 3, 1, 1, activation=activation_head, momentum=momentum),
                    lnn.layer.Conv2dBatchAct(co*2, co, 1, 1, 0, activation=activation_head, momentum=momentum),
                ),
            ),
        ])

        self.head = nn.ModuleDict()
        if self.outputs[0]:
            self.head['0'] = lnn.head.DetectionYoloAnchor(
                512,
                self.anchors.get_scale(len(self.head)).num_anchors,
                self.num_classes,
                1024,
                activation=activation_head,
                momentum=momentum,
            )
        if self.outputs[1]:
            self.head['1'] = lnn.head.DetectionYoloAnchor(
                256,
                self.anchors.get_scale(len(self.head)).num_anchors,
                self.num_classes,
                512,
                activation=activation_head,
                momentum=momentum,
            )
        if self.outputs[2]:
            self.head['2'] = lnn.head.DetectionYoloAnchor(
                128,
                self.anchors.get_scale(len(self.head)).num_anchors,
                self.num_classes,
                256,
                activation=activation_head,
                momentum=momentum,
            )

    def __init_weights__(self, name, mod):
        if isinstance(mod, nn.Conv2d):
            nn.init.kaiming_normal_(mod.weight, nonlinearity='leaky_relu', a=0.1)
            if mod.bias is not None:
                nn.init.constant_(mod.bias, 0)
            return True

        return super().__init_weights__(name, mod)

    def forward(self, x):
        csp_11, csp_9, csp_7 = self.backbone(x)

        csp_11 = self.neck[0](csp_11)
        outputs = self.neck[1](csp_11, csp_9, csp_7)

        outputs = [head(outputs[int(idx)]) for idx, head in self.head.items()]

        if len(outputs) == 1:
            return outputs[0]
        return outputs

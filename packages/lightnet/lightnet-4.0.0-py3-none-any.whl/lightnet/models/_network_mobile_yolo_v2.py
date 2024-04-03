#
#   Mobile YOLOv2 model
#   Copyright EAVISE
#
import functools
import torch
import torch.nn as nn
import lightnet as ln
import lightnet.network as lnn

__all__ = ['MobileYoloV2']


class MobileYoloV2(lnn.module.Darknet):
    """ Yolo v2 implementation with depthwise separable convolutions :cite:`optim_detection`.

    Args:
        num_classes (int): Number of classes
        input_channels (int, optional): Number of input channels; Default **3**
        anchors (ln.util.Anchors, optional): single-scale list of anchor boxes; Default **Darknet YoloV2 VOC**

    Attributes:
        self.stride: Subsampling factor of the network (input_dim / output_dim)
        self.inner_stride: Maximal internal subsampling factor of the network (input dimension should be a multiple of this)
        self.remap_mobile_darknet19: Remapping rules for weights from the :class:`~lightnet.models.MobileDarknet19` model.
        self.remap_v1: Remapping rules for weightfiles created with lightnet prior to v3.0.0

    Note:
        The preferred way to pass anchors is to use the :class:`~lightnet.util.Anchors`.
        However, for compatibility reasons, you can also pass in a list of tuples,
        which will be interpreted as darknet anchors (relative to output dimensions).
    """
    stride = 32
    inner_stride = 32
    remap_mobile_darknet19 = (
        (r'^backbone\.(.*)',   r'backbone.module.\1'),
    )

    MODEL_VERSION = 1
    remap_v1 = (
        (r'^layers.3.24_convbatch.(.*)', r'head.0.\1'),
        (r'^layers.3.25_conv.(.*)', r'head.1.\1'),
        (r'^layers.1.20_convdw.(.*)', r'neck.0.0.\1'),
        (r'^layers.1.21_convdw.(.*)', r'neck.0.1.\1'),
        (r'^layers.2.22_convbatch.(.*)', r'neck.1.0.\1'),
        (r'^layers.0.(.*)', r'backbone.module.\1'),
        (r'^layers.1.(.*)', r'backbone.module.\1'),
    )

    def __init_module__(
        self,
        num_classes,
        input_channels=3,
        anchors=ln.util.Anchors.YoloV2_VOC,
    ):
        if not isinstance(anchors, ln.util.Anchors):
            anchors = ln.util.Anchors.from_darknet(self, anchors)
        if anchors.num_scales != 1:
            raise ln.util.AnchorError(anchors, f'Expected 1 scale, but got {anchors.num_scales}')
        if anchors.values_per_anchor != 2:
            raise ln.util.AnchorError(anchors, f'Expected 2 values per anchor, but got {anchors.values_per_anchor}')

        self.num_classes = num_classes
        self.input_channels = input_channels
        self.anchors = anchors

        # Network
        activation = functools.partial(nn.LeakyReLU, 0.1, inplace=True)
        momentum = 0.01

        self.backbone = lnn.layer.FeatureExtractor(
            lnn.backbone.MobileDarknet.DN_19(input_channels, 1024, activation=activation, momentum=momentum),
            ['13_convdw'],
            True,
        )

        self.neck = nn.ModuleList([
            nn.Sequential(
                lnn.layer.Conv2dDepthWise(1024, 1024, 3, 1, 1, activation=activation, momentum=momentum),
                lnn.layer.Conv2dDepthWise(1024, 1024, 3, 1, 1, activation=activation, momentum=momentum),
            ),
            nn.Sequential(
                lnn.layer.Conv2dBatchAct(512, 64, 1, 1, 0, activation=activation, momentum=momentum),
                lnn.layer.Reorg(2),
            ),
        ])

        self.head = lnn.head.DetectionYoloAnchor(
            (4*64)+1024,
            self.anchors.num_anchors,
            self.num_classes,
            activation=activation,
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
        x, feat_13 = self.backbone(x)

        x = self.neck[0](x)
        feat_13 = self.neck[1](feat_13)

        x = self.head(torch.cat((feat_13, x), 1))

        return x

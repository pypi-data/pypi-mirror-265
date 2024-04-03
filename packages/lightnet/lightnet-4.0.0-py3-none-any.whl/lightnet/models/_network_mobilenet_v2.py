#
#   MobileNet classification network
#   Copyright EAVISE
#
import lightnet.network as lnn

__all__ = ['MobilenetV2']


class MobilenetV2(lnn.module.Lightnet):
    """ Mobilenet v2 classification network implementation :cite:`mobilenet_v2`.

    Args:
        num_classes (int): Number of classes
        alpha (int, optional): Number between [0-1] that controls the number of filters of the mobilenet convolutions; Default **1**
        input_channels (int, optional): Number of input channels; Default **3**
        dropout (float, optional): Probability of the dropout layers in the classification head; Default **0.5**

    Attributes:
        self.inner_stride: Maximal internal subsampling factor of the network (input dimension should be a multiple of this)
        self.remap_v1: Remapping rules for weightfiles created with lightnet prior to v3.0.0

    Warning:
        When changing the ``alpha`` value, you are changing the network architecture.
        This means you cannot use weights from this network with a different alpha value.

    Note:
        The average pooling is implemented with an :class:`~torch.nn.AdaptiveAvgPool2d` layer. |br|
        For the base input dimension of 224x224, this is exactly the same as a 7x7 average pooling function,
        but the advantage of a adaptive average pooling is that this network can now handle multiple different input dimensions,
        as long as they are a multiple of the ``stride`` factor. |br|
        This is also how the implementation in `tensorflow <mobilenetv2tf_>`_ works.

    .. _mobilenetv2tf: https://github.com/tensorflow/models/blob/505f554c6417931c96b59516f14d1ad65df6dbc5/research/slim/nets/mobilenet/mobilenet.py#L365
    """
    inner_stride = 32

    MODEL_VERSION = 1
    remap_v1 = (
        (r'^layers.0.(.*)', r'backbone.\1'),
        (r'^layers.1.22_conv.(.*)', r'head.2.\1'),
    )

    def __init_module__(
        self,
        num_classes,
        alpha=1,
        input_channels=3,
        dropout=0.5,
    ):
        self.num_classes = num_classes
        self.alpha = alpha
        self.input_channels = input_channels

        # Network
        self.backbone = lnn.backbone.Mobilenet.V2(input_channels, int(alpha*1280), alpha)
        self.head = lnn.head.ClassificationConv(int(alpha*1280), num_classes, dropout=dropout)

    def forward(self, x):
        x = self.backbone(x)
        x = self.head(x)

        return x

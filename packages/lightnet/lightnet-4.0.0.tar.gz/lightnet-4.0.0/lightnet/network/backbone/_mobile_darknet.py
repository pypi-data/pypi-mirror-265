#
#   MobileDarknet Backbone
#   Copyright EAVISE
#
from functools import partial
import torch.nn as nn
from .. import layer as lnl
from .._basemodule import BaseModule

__all__ = ['MobileDarknet']


class MobileDarknet(BaseModule):
    """
    MobileDarknet backbones. |br|
    We replace all 3x3 convolution with depthwise separable variants and remove all possible max-pooling layers, using strided convolutions instead.
    """
    default_activation = partial(nn.LeakyReLU, 0.1, inplace=True)

    @BaseModule.layers(named=True, primary=True)
    def DN(in_channels, out_channels, momentum=0.01, activation=default_activation, relu=None):
        """
        Base Darknet backbone.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            momentum (float, optional): Momentum of the moving averages of the normalization; Default **0.01**
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.LeakyReLU(0.1)`

        Examples:
            >>> backbone = ln.network.backbone.MobileDarknet(3, 1024)
            >>> print(backbone)
            Sequential(
              (1_convbatch): Conv2dBatchAct(3, 16, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (2_convdw): Conv2dDepthWise(16, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (3_convdw): Conv2dDepthWise(32, 64, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (4_convdw): Conv2dDepthWise(64, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (5_convdw): Conv2dDepthWise(128, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (6_convdw): Conv2dDepthWise(256, 1024, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 1024, 20, 20])

        .. deprecated:: 4.0.0
            |br| The `relu` argument is deprecated in favor for the more generic name "activation".
        """
        if relu is not None:
            import warnings
            warnings.warn(
                'The "relu" argument is deprecated in favor for the more generic name "activation"',
                category=DeprecationWarning,
                stacklevel=2,
            )
            activation = relu

        return (
            ('1_convbatch',     lnl.Conv2dBatchAct(in_channels, 16, 3, 2, 1, activation=activation, momentum=momentum)),
            ('2_convdw',        lnl.Conv2dDepthWise(16, 32, 3, 2, 1, activation=activation, momentum=momentum)),
            ('3_convdw',        lnl.Conv2dDepthWise(32, 64, 3, 2, 1, activation=activation, momentum=momentum)),
            ('4_convdw',        lnl.Conv2dDepthWise(64, 128, 3, 2, 1, activation=activation, momentum=momentum)),
            ('5_convdw',        lnl.Conv2dDepthWise(128, 256, 3, 2, 1, activation=activation, momentum=momentum)),
            ('6_convdw',        lnl.Conv2dDepthWise(256, out_channels, 3, 1, 1, activation=activation, momentum=momentum)),
        )

    @BaseModule.layers(named=True)
    def DN_19(in_channels, out_channels, momentum=0.01, activation=default_activation, relu=None):
        """
        Darknet19 backbone.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            momentum (float, optional): Momentum of the moving averages of the normalization; Default **0.01**
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.LeakyReLU(0.1)`

        .. rubric:: Models:

        - :class:`~lightnet.models.MobileDarknet19`
        - :class:`~lightnet.models.MobileYoloV2`
        - :class:`~lightnet.models.MobileYoloV2Upsample`

        Examples:
            >>> backbone = ln.network.backbone.MobileDarknet.DN_19(3, 1024)
            >>> print(backbone)
            Sequential(
              (1_convbatch): Conv2dBatchAct(3, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (2_convdw): Conv2dDepthWise(32, 64, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (3_convdw): Conv2dDepthWise(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (4_convbatch): Conv2dBatchAct(128, 64, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), LeakyReLU(negative_slope=0.1, inplace=True))
              (5_convdw): Conv2dDepthWise(64, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (6_convdw): Conv2dDepthWise(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (7_convbatch): Conv2dBatchAct(256, 128, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), LeakyReLU(negative_slope=0.1, inplace=True))
              (8_convdw): Conv2dDepthWise(128, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (9_convdw): Conv2dDepthWise(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (10_convbatch): Conv2dBatchAct(512, 256, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), LeakyReLU(negative_slope=0.1, inplace=True))
              (11_convdw): Conv2dDepthWise(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (12_convbatch): Conv2dBatchAct(512, 256, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), LeakyReLU(negative_slope=0.1, inplace=True))
              (13_convdw): Conv2dDepthWise(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (14_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (15_convdw): Conv2dDepthWise(512, 1024, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (16_convbatch): Conv2dBatchAct(1024, 512, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), LeakyReLU(negative_slope=0.1, inplace=True))
              (17_convdw): Conv2dDepthWise(512, 1024, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (18_convbatch): Conv2dBatchAct(1024, 512, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), LeakyReLU(negative_slope=0.1, inplace=True))
              (19_convdw): Conv2dDepthWise(512, 1024, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 1024, 20, 20])

        .. deprecated:: 4.0.0
            |br| The `relu` argument is deprecated in favor for the more generic name "activation".
        """
        if relu is not None:
            import warnings
            warnings.warn(
                'The "relu" argument is deprecated in favor for the more generic name "activation"',
                category=DeprecationWarning,
                stacklevel=2,
            )
            activation = relu

        return (
            ('1_convbatch',     lnl.Conv2dBatchAct(in_channels, 32, 3, 2, 1, activation=activation, momentum=momentum)),
            ('2_convdw',        lnl.Conv2dDepthWise(32, 64, 3, 2, 1, activation=activation, momentum=momentum)),
            ('3_convdw',        lnl.Conv2dDepthWise(64, 128, 3, 1, 1, activation=activation, momentum=momentum)),
            ('4_convbatch',     lnl.Conv2dBatchAct(128, 64, 1, 1, 0, activation=activation, momentum=momentum)),
            ('5_convdw',        lnl.Conv2dDepthWise(64, 128, 3, 2, 1, activation=activation, momentum=momentum)),
            ('6_convdw',        lnl.Conv2dDepthWise(128, 256, 3, 1, 1, activation=activation, momentum=momentum)),
            ('7_convbatch',     lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum)),
            ('8_convdw',        lnl.Conv2dDepthWise(128, 256, 3, 2, 1, activation=activation, momentum=momentum)),
            ('9_convdw',        lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum)),
            ('10_convbatch',    lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum)),
            ('11_convdw',       lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum)),
            ('12_convbatch',    lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum)),
            ('13_convdw',       lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum)),
            ('14_max',          nn.MaxPool2d(2, 2)),
            ('15_convdw',       lnl.Conv2dDepthWise(512, 1024, 3, 1, 1, activation=activation, momentum=momentum)),
            ('16_convbatch',    lnl.Conv2dBatchAct(1024, 512, 1, 1, 0, activation=activation, momentum=momentum)),
            ('17_convdw',       lnl.Conv2dDepthWise(512, 1024, 3, 1, 1, activation=activation, momentum=momentum)),
            ('18_convbatch',    lnl.Conv2dBatchAct(1024, 512, 1, 1, 0, activation=activation, momentum=momentum)),
            ('19_convdw',       lnl.Conv2dDepthWise(512, out_channels, 3, 1, 1, activation=activation, momentum=momentum)),
        )

    @BaseModule.layers(named=True)
    def DN_53(in_channels, out_channels, momentum=0.01, activation=default_activation, relu=None):
        """
        Darknet53 backbone.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            momentum (float, optional): Momentum of the moving averages of the normalization; Default **0.01**
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.LeakyReLU(0.1)`

        Examples:
            >>> backbone = ln.network.backbone.MobileDarknet.DN_53(3, 1024)
            >>> print(backbone)
            Sequential(
              (1_convbatch): Conv2dBatchAct(3, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (2_convbatch): Conv2dDepthWise(32, 64, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (3_residual): Residual(...)
              (4_convbatch): Conv2dDepthWise(64, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (5_residual): Residual(...)
              (6_residual): Residual(...)
              (7_convbatch): Conv2dDepthWise(128, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (8_residual): Residual(...)
              (9_residual): Residual(...)
              (10_residual): Residual(...)
              (11_residual): Residual(...)
              (12_residual): Residual(...)
              (13_residual): Residual(...)
              (14_residual): Residual(...)
              (15_residual): Residual(...)
              (16_convbatch): Conv2dDepthWise(256, 512, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (17_residual): Residual(...)
              (18_residual): Residual(...)
              (19_residual): Residual(...)
              (20_residual): Residual(...)
              (21_residual): Residual(...)
              (22_residual): Residual(...)
              (23_residual): Residual(...)
              (24_residual): Residual(...)
              (25_convbatch): Conv2dDepthWise(512, 1024, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
              (26_residual): Residual(...)
              (27_residual): Residual(...)
              (28_residual): Residual(...)
              (29_residual): Residual(...)
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 1024, 20, 20])

        .. deprecated:: 4.0.0
            |br| The `relu` argument is deprecated in favor for the more generic name "activation".
        """
        if relu is not None:
            import warnings
            warnings.warn(
                'The "relu" argument is deprecated in favor for the more generic name "activation"',
                category=DeprecationWarning,
                stacklevel=2,
            )
            activation = relu

        return (
            ('1_convbatch',         lnl.Conv2dBatchAct(in_channels, 32, 3, 1, 1, activation=activation, momentum=momentum)),
            ('2_convbatch',         lnl.Conv2dDepthWise(32, 64, 3, 2, 1, activation=activation, momentum=momentum)),
            ('3_residual',          lnl.Residual(
                                    lnl.Conv2dBatchAct(64, 32, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(32, 64, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('4_convbatch',         lnl.Conv2dDepthWise(64, 128, 3, 2, 1, activation=activation, momentum=momentum)),
            ('5_residual',          lnl.Residual(
                                    lnl.Conv2dBatchAct(128, 64, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(64, 128, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('6_residual',          lnl.Residual(
                                    lnl.Conv2dBatchAct(128, 64, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(64, 128, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('7_convbatch',         lnl.Conv2dDepthWise(128, 256, 3, 2, 1, activation=activation, momentum=momentum)),
            ('8_residual',          lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(128, 256, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('9_residual',          lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(128, 256, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('10_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(128, 256, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('11_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(128, 256, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('12_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(128, 256, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('13_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(128, 256, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('14_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(128, 256, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('15_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(128, 256, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('16_convbatch',        lnl.Conv2dDepthWise(256, 512, 3, 2, 1, activation=activation, momentum=momentum)),
            ('17_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('18_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('19_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('20_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('21_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('22_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('23_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('24_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(256, 512, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('25_convbatch',        lnl.Conv2dDepthWise(512, out_channels, 3, 2, 1, activation=activation, momentum=momentum)),
            ('26_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(out_channels, 512, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(512, out_channels, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('27_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(out_channels, 512, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(512, out_channels, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('28_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(out_channels, 512, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(512, out_channels, 3, 1, 1, activation=activation, momentum=momentum),
            )),
            ('29_residual',         lnl.Residual(
                                    lnl.Conv2dBatchAct(out_channels, 512, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dDepthWise(512, out_channels, 3, 1, 1, activation=activation, momentum=momentum),
            )),
        )

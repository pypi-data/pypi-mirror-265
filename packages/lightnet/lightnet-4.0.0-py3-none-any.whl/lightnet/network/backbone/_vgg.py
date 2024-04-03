#
#   VGG Backbone
#   Copyright EAVISE
#
from functools import partial
import torch.nn as nn
from .. import layer as lnl
from .._basemodule import BaseModule

__all__ = ['VGG']


class VGG(BaseModule):
    """ VGG backbones. """
    default_activation = partial(nn.ReLU, inplace=True)

    @BaseModule.layers(named=True)
    def A(
        in_channels,
        out_channels,
        batch_norm=False,
        activation=default_activation,
        relu=None,
    ):
        """
        Configuration A from the VGG paper.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            batch_norm (bool, optional): Whether or not to have a batchnorm after each convolution; Default **False**
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.ReLU`

        .. rubric:: Models:

        - :class:`~lightnet.models.VGG11`

        Examples:
            >>> backbone = ln.network.backbone.VGG.A(3, 512)
            >>> print(backbone)
            Sequential(
              (1_conv): Conv2dAct(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (2_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (3_conv): Conv2dAct(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (4_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (5_conv): Conv2dAct(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (6_conv): Conv2dAct(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (7_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (8_conv): Conv2dAct(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (9_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (10_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (11_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (12_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (13_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 512, 20, 20])

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

        layer = lnl.Conv2dBatchAct if batch_norm else lnl.Conv2dAct
        return (
            ('1_conv',      layer(in_channels, 64, 3, 1, 1, bias=True, activation=activation)),
            ('2_max',       nn.MaxPool2d(2, 2)),
            ('3_conv',      layer(64, 128, 3, 1, 1, bias=True, activation=activation)),
            ('4_max',       nn.MaxPool2d(2, 2)),
            ('5_conv',      layer(128, 256, 3, 1, 1, bias=True, activation=activation)),
            ('6_conv',      layer(256, 256, 3, 1, 1, bias=True, activation=activation)),
            ('7_max',       nn.MaxPool2d(2, 2)),
            ('8_conv',      layer(256, 512, 3, 1, 1, bias=True, activation=activation)),
            ('9_conv',      layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('10_max',      nn.MaxPool2d(2, 2)),
            ('11_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('12_conv',     layer(512, out_channels, 3, 1, 1, bias=True, activation=activation)),
            ('13_max',      nn.MaxPool2d(2, 2)),
        )

    @BaseModule.layers(named=True)
    def B(
        in_channels,
        out_channels,
        batch_norm=False,
        activation=default_activation,
        relu=None,
    ):
        """
        Configuration B from the VGG paper.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            batch_norm (bool, optional): Whether or not to have a batchnorm after each convolution; Default **False**
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.ReLU`

        .. rubric:: Models:

        - :class:`~lightnet.models.VGG13`

        Examples:
            >>> backbone = ln.network.backbone.VGG.B(3, 512)
            >>> print(backbone)
            Sequential(
              (1_conv): Conv2dAct(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (2_conv): Conv2dAct(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (3_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (4_conv): Conv2dAct(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (5_conv): Conv2dAct(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (6_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (7_conv): Conv2dAct(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (8_conv): Conv2dAct(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (9_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (10_conv): Conv2dAct(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (11_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (12_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (13_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (14_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (15_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 512, 20, 20])

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

        layer = lnl.Conv2dBatchAct if batch_norm else lnl.Conv2dAct
        return (
            ('1_conv',      layer(in_channels, 64, 3, 1, 1, bias=True, activation=activation)),
            ('2_conv',      layer(64, 64, 3, 1, 1, bias=True, activation=activation)),
            ('3_max',       nn.MaxPool2d(2, 2)),
            ('4_conv',      layer(64, 128, 3, 1, 1, bias=True, activation=activation)),
            ('5_conv',      layer(128, 128, 3, 1, 1, bias=True, activation=activation)),
            ('6_max',       nn.MaxPool2d(2, 2)),
            ('7_conv',      layer(128, 256, 3, 1, 1, bias=True, activation=activation)),
            ('8_conv',      layer(256, 256, 3, 1, 1, bias=True, activation=activation)),
            ('9_max',       nn.MaxPool2d(2, 2)),
            ('10_conv',     layer(256, 512, 3, 1, 1, bias=True, activation=activation)),
            ('11_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('12_max',      nn.MaxPool2d(2, 2)),
            ('13_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('14_conv',     layer(512, out_channels, 3, 1, 1, bias=True, activation=activation)),
            ('15_max',      nn.MaxPool2d(2, 2)),
        )

    @BaseModule.layers(named=True)
    def C(
        in_channels,
        out_channels,
        batch_norm=False,
        activation=default_activation,
        relu=None,
    ):
        """
        Configuration C from the VGG paper.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            batch_norm (bool, optional): Whether or not to have a batchnorm after each convolution; Default **False**
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.ReLU`

        Examples:
            >>> backbone = ln.network.backbone.VGG.C(3, 512)
            >>> print(backbone)
            Sequential(
              (1_conv): Conv2dAct(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (2_conv): Conv2dAct(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (3_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (4_conv): Conv2dAct(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (5_conv): Conv2dAct(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (6_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (7_conv): Conv2dAct(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (8_conv): Conv2dAct(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (9_conv): Conv2dAct(256, 256, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
              (10_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (11_conv): Conv2dAct(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (12_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (13_conv): Conv2dAct(512, 512, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
              (14_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (15_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (16_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (17_conv): Conv2dAct(512, 512, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
              (18_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 512, 20, 20])

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

        layer = lnl.Conv2dBatchAct if batch_norm else lnl.Conv2dAct
        return (
            ('1_conv',      layer(in_channels, 64, 3, 1, 1, bias=True, activation=activation)),
            ('2_conv',      layer(64, 64, 3, 1, 1, bias=True, activation=activation)),
            ('3_max',       nn.MaxPool2d(2, 2)),
            ('4_conv',      layer(64, 128, 3, 1, 1, bias=True, activation=activation)),
            ('5_conv',      layer(128, 128, 3, 1, 1, bias=True, activation=activation)),
            ('6_max',       nn.MaxPool2d(2, 2)),
            ('7_conv',      layer(128, 256, 3, 1, 1, bias=True, activation=activation)),
            ('8_conv',      layer(256, 256, 3, 1, 1, bias=True, activation=activation)),
            ('9_conv',      layer(256, 256, 1, 1, 0, bias=True, activation=activation)),
            ('10_max',      nn.MaxPool2d(2, 2)),
            ('11_conv',     layer(256, 512, 3, 1, 1, bias=True, activation=activation)),
            ('12_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('13_conv',     layer(512, 512, 1, 1, 0, bias=True, activation=activation)),
            ('14_max',      nn.MaxPool2d(2, 2)),
            ('15_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('16_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('17_conv',     layer(512, out_channels, 1, 1, 0, bias=True, activation=activation)),
            ('18_max',      nn.MaxPool2d(2, 2)),
        )

    @BaseModule.layers(named=True)
    def D(
        in_channels,
        out_channels,
        batch_norm=False,
        activation=default_activation,
        relu=None,
    ):
        """
        Configuration D from the VGG paper.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            batch_norm (bool, optional): Whether or not to have a batchnorm after each convolution; Default **False**
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.ReLU`

        .. rubric:: Models:

        - :class:`~lightnet.models.VGG16`

        Examples:
            >>> backbone = ln.network.backbone.VGG.D(3, 512)
            >>> print(backbone)
            Sequential(
              (1_conv): Conv2dAct(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (2_conv): Conv2dAct(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (3_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (4_conv): Conv2dAct(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (5_conv): Conv2dAct(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (6_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (7_conv): Conv2dAct(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (8_conv): Conv2dAct(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (9_conv): Conv2dAct(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (10_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (11_conv): Conv2dAct(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (12_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (13_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (14_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (15_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (16_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (17_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (18_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 512, 20, 20])

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

        layer = lnl.Conv2dBatchAct if batch_norm else lnl.Conv2dAct
        return (
            ('1_conv',      layer(in_channels, 64, 3, 1, 1, bias=True, activation=activation)),
            ('2_conv',      layer(64, 64, 3, 1, 1, bias=True, activation=activation)),
            ('3_max',       nn.MaxPool2d(2, 2)),
            ('4_conv',      layer(64, 128, 3, 1, 1, bias=True, activation=activation)),
            ('5_conv',      layer(128, 128, 3, 1, 1, bias=True, activation=activation)),
            ('6_max',       nn.MaxPool2d(2, 2)),
            ('7_conv',      layer(128, 256, 3, 1, 1, bias=True, activation=activation)),
            ('8_conv',      layer(256, 256, 3, 1, 1, bias=True, activation=activation)),
            ('9_conv',      layer(256, 256, 3, 1, 1, bias=True, activation=activation)),
            ('10_max',      nn.MaxPool2d(2, 2)),
            ('11_conv',     layer(256, 512, 3, 1, 1, bias=True, activation=activation)),
            ('12_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('13_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('14_max',      nn.MaxPool2d(2, 2)),
            ('15_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('16_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('17_conv',     layer(512, out_channels, 3, 1, 1, bias=True, activation=activation)),
            ('18_max',      nn.MaxPool2d(2, 2)),
        )

    @BaseModule.layers(named=True)
    def E(
        in_channels,
        out_channels,
        batch_norm=False,
        activation=default_activation,
        relu=None,
    ):
        """
        Configuration E from the VGG paper.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            batch_norm (bool, optional): Whether or not to have a batchnorm after each convolution; Default **False**
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.ReLU`

        .. rubric:: Models:

        - :class:`~lightnet.models.VGG19`

        Examples:
            >>> backbone = ln.network.backbone.VGG.E(3, 512)
            >>> print(backbone)
            Sequential(
              (1_conv): Conv2dAct(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (2_conv): Conv2dAct(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (3_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (4_conv): Conv2dAct(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (5_conv): Conv2dAct(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (6_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (7_conv): Conv2dAct(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (8_conv): Conv2dAct(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (9_conv): Conv2dAct(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (10_conv): Conv2dAct(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (11_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (12_conv): Conv2dAct(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (13_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (14_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (15_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (16_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (17_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (18_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (19_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (20_conv): Conv2dAct(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
              (21_max): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 512, 20, 20])

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

        layer = lnl.Conv2dBatchAct if batch_norm else lnl.Conv2dAct
        return (
            ('1_conv',      layer(in_channels, 64, 3, 1, 1, bias=True, activation=activation)),
            ('2_conv',      layer(64, 64, 3, 1, 1, bias=True, activation=activation)),
            ('3_max',       nn.MaxPool2d(2, 2)),
            ('4_conv',      layer(64, 128, 3, 1, 1, bias=True, activation=activation)),
            ('5_conv',      layer(128, 128, 3, 1, 1, bias=True, activation=activation)),
            ('6_max',       nn.MaxPool2d(2, 2)),
            ('7_conv',      layer(128, 256, 3, 1, 1, bias=True, activation=activation)),
            ('8_conv',      layer(256, 256, 3, 1, 1, bias=True, activation=activation)),
            ('9_conv',      layer(256, 256, 3, 1, 1, bias=True, activation=activation)),
            ('10_conv',     layer(256, 256, 3, 1, 1, bias=True, activation=activation)),
            ('11_max',      nn.MaxPool2d(2, 2)),
            ('12_conv',     layer(256, 512, 3, 1, 1, bias=True, activation=activation)),
            ('13_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('14_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('15_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('16_max',      nn.MaxPool2d(2, 2)),
            ('17_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('18_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('19_conv',     layer(512, 512, 3, 1, 1, bias=True, activation=activation)),
            ('20_conv',     layer(512, out_channels, 3, 1, 1, bias=True, activation=activation)),
            ('21_max',      nn.MaxPool2d(2, 2)),
        )

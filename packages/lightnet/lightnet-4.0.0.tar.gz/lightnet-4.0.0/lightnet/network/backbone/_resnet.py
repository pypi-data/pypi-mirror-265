#
#   Resnet Backbone
#   Copyright EAVISE
#
from functools import partial
import torch.nn as nn
from .. import layer as lnl
from .._basemodule import BaseModule

__all__ = ['Resnet', 'DeformableResnet', 'ModulatedResnet']


class Resnet(BaseModule):
    """ Resnet Backbones. """
    default_activation = partial(nn.ReLU, inplace=True)
    conv_type1 = nn.Conv2d
    conv_type2 = nn.Conv2d

    @staticmethod
    def get_residual(conv_type):
        """ Basic residual block used in Resnet18 and Resnet34. """
        def residual(in_channels, out_channels, stride, activation):
            return lnl.Residual(
                lnl.Conv2dBatchAct(in_channels, out_channels, 3, stride, 1, activation=activation, conv=conv_type),
                lnl.Conv2dBatch(out_channels, out_channels, 3, 1, 1, conv=conv_type),

                skip=None if (in_channels == out_channels) and (stride == 1) else lnl.Conv2dBatch(in_channels, out_channels, 1, stride, 0),
                post=activation(),
            )

        return residual

    @staticmethod
    def get_bottleneck(conv_type):
        """ Bottleneck residual block used in the deeper Resnet50, Resnet101 and Resnet152 architectures. """
        def bottleneck(in_channels, inter_channels, out_channels, stride, activation):
            return lnl.Residual(
                lnl.Conv2dBatchAct(in_channels, inter_channels, 1, 1, 0, activation=activation),
                lnl.Conv2dBatchAct(inter_channels, inter_channels, 3, stride, 1, activation=activation, conv=conv_type),
                lnl.Conv2dBatch(inter_channels, out_channels, 1, 1, 0),

                skip=None if (in_channels == out_channels) and (stride == 1) else lnl.Conv2dBatch(in_channels, out_channels, 1, stride, 0),
                post=activation(),
            )

        return bottleneck

    @BaseModule.layers(named=True, classmethod=True)
    def RN_18(
        cls,
        in_channels,
        out_channels,
        activation=default_activation,
    ):
        """
        ResNet18 backbone.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.ReLU`

        .. rubric:: Models:

        - :class:`~lightnet.models.Resnet18`

        Example:
            >>> backbone = ln.network.backbone.Resnet.RN_18(3, 512)
            >>> print(backbone)     # doctest: +SKIP
            Sequential(
              (1_convbatch): Conv2dBatchAct(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), ReLU(inplace=True))
              (2_max): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
              (3_residual): Residual(
                (1): Conv2dBatchAct(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
                (2): Conv2dBatch(64, 64, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0))
                (post): ReLU(inplace=True)
              )
              (4_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
              )
              (5_residual): Residual(...)
              (6_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
                (2): Residual(...)
              )
              (7_residual): Residual(...)
              (8_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
                (2): Residual(...)
                (3): Residual(...)
                (4): Residual(...)
              )
              (9_residual): Residual(...)
              (10_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
              )
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 512, 20, 20])
        """
        groups = (1, 1, 1, 1)
        get_block1 = cls.get_residual(cls.conv_type1)
        get_block2 = cls.get_residual(cls.conv_type2)

        return (
            # Conv 1
            ('1_convbatch',         lnl.Conv2dBatchAct(in_channels, 64, 7, 2, 3, activation=activation)),
            ('2_max',               nn.MaxPool2d(3, 2, 1)),

            # Conv 2_x
            ('3_residual',          get_block1(64, 64, 1, activation)),
            ('4_residualgroup',     nn.Sequential(*(groups[0]*[get_block1(64, 64, 1, activation)]))),

            # Conv 3_x
            ('5_residual',          get_block2(64, 128, 2, activation)),
            ('6_residualgroup',     nn.Sequential(*(groups[1]*[get_block2(128, 128, 1, activation)]))),

            # Conv 4_x
            ('7_residual',          get_block2(128, 256, 2, activation)),
            ('8_residualgroup',     nn.Sequential(*(groups[2]*[get_block2(256, 256, 1, activation)]))),

            # Conv 5_x
            ('9_residual',          get_block2(256, out_channels, 2, activation)),
            ('10_residualgroup',    nn.Sequential(*(groups[3]*[get_block2(out_channels, out_channels, 1, activation)]))),
        )

    @BaseModule.layers(named=True, classmethod=True)
    def RN_34(
        cls,
        in_channels,
        out_channels,
        activation=default_activation,
    ):
        """
        ResNet34 backbone.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.ReLU`

        .. rubric:: Models:

        - :class:`~lightnet.models.Resnet34`

        Example:
            >>> backbone = ln.network.backbone.Resnet.RN_34(3, 512)
            >>> print(backbone)     # doctest: +SKIP
            Sequential(
              (1_convbatch): Conv2dBatchAct(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), ReLU(inplace=True))
              (2_max): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
              (3_residual): Residual(
                (1): Conv2dBatchAct(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
                (2): Conv2dBatch(64, 64, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0))
                (post): ReLU(inplace=True)
              )
              (4_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
              )
              (5_residual): Residual(...)
              (6_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
                (2): Residual(...)
              )
              (7_residual): Residual(...)
              (8_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
                (2): Residual(...)
                (3): Residual(...)
                (4): Residual(...)
              )
              (9_residual): Residual(...)
              (10_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
              )
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 512, 20, 20])
        """
        groups = (2, 3, 5, 2)
        get_block1 = cls.get_residual(cls.conv_type1)
        get_block2 = cls.get_residual(cls.conv_type2)

        return (
            # Conv 1
            ('1_convbatch',         lnl.Conv2dBatchAct(in_channels, 64, 7, 2, 3, activation=activation)),
            ('2_max',               nn.MaxPool2d(3, 2, 1)),

            # Conv 2_x
            ('3_residual',          get_block1(64, 64, 1, activation)),
            ('4_residualgroup',     nn.Sequential(*(groups[0]*[get_block1(64, 64, 1, activation)]))),

            # Conv 3_x
            ('5_residual',          get_block2(64, 128, 2, activation)),
            ('6_residualgroup',     nn.Sequential(*(groups[1]*[get_block2(128, 128, 1, activation)]))),

            # Conv 4_x
            ('7_residual',          get_block2(128, 256, 2, activation)),
            ('8_residualgroup',     nn.Sequential(*(groups[2]*[get_block2(256, 256, 1, activation)]))),

            # Conv 5_x
            ('9_residual',          get_block2(256, out_channels, 2, activation)),
            ('10_residualgroup',    nn.Sequential(*(groups[3]*[get_block2(out_channels, out_channels, 1, activation)]))),
        )

    @BaseModule.layers(named=True, classmethod=True)
    def RN_50(
        cls,
        in_channels,
        out_channels,
        activation=default_activation,
    ):
        """
        ResNet50 backbone.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.ReLU`

        .. rubric:: Models:

        - :class:`~lightnet.models.Resnet50`
        - :class:`~lightnet.models.ResnetYolo`
        - :class:`~lightnet.models.M_ResnetYolo`

        Example:
            >>> backbone = ln.network.backbone.Resnet.RN_50(3, 2048)
            >>> print(backbone)     # doctest: +SKIP
            Sequential(
              (1_convbatch): Conv2dBatchAct(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), ReLU(inplace=True))
              (2_max): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
              (3_residual): Residual(
                (0): Conv2dBatchAct(64, 64, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
                (1): Conv2dBatchAct(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
                (2): Conv2dBatch(64, 256, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0))
                (skip): Conv2dBatch(64, 256, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0))
                (post): ReLU(inplace=True)
              )
              (4_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
              )
              (5_residual): Residual(...)
              (6_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
                (2): Residual(...)
              )
              (7_residual): Residual(...)
              (8_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
                (2): Residual(...)
                (3): Residual(...)
                (4): Residual(...)
              )
              (9_residual): Residual(...)
              (10_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
              )
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 2048, 20, 20])
        """
        groups = (2, 3, 5, 2)
        get_block1 = cls.get_bottleneck(cls.conv_type1)
        get_block2 = cls.get_bottleneck(cls.conv_type2)

        return (
            # Conv 1
            ('1_convbatch',         lnl.Conv2dBatchAct(in_channels, 64, 7, 2, 3, activation=activation)),
            ('2_max',               nn.MaxPool2d(3, 2, 1)),

            # Conv 2_x
            ('3_residual',          get_block1(64, 64, 256, 1, activation)),
            ('4_residualgroup',     nn.Sequential(*(groups[0]*[get_block1(256, 64, 256, 1, activation)]))),

            # Conv 3_x
            ('5_residual',          get_block2(256, 128, 512, 2, activation)),
            ('6_residualgroup',     nn.Sequential(*(groups[1]*[get_block2(512, 128, 512, 1, activation)]))),

            # Conv 4_x
            ('7_residual',          get_block2(512, 256, 1024, 2, activation)),
            ('8_residualgroup',     nn.Sequential(*(groups[2]*[get_block2(1024, 256, 1024, 1, activation)]))),

            # Conv 5_x
            ('9_residual',          get_block2(1024, 512, out_channels, 2, activation)),
            ('10_residualgroup',    nn.Sequential(*(groups[3]*[get_block2(out_channels, 512, out_channels, 1, activation)]))),
        )

    @BaseModule.layers(named=True, classmethod=True)
    def RN_101(
        cls,
        in_channels,
        out_channels,
        activation=default_activation,
    ):
        """
        ResNet101 backbone.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.ReLU`

        .. rubric:: Models:

        - :class:`~lightnet.models.Resnet101`

        Example:
            >>> backbone = ln.network.backbone.Resnet.RN_101(3, 2048)
            >>> print(backbone)     # doctest: +SKIP
            Sequential(
              (1_convbatch): Conv2dBatchAct(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), ReLU(inplace=True))
              (2_max): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
              (3_residual): Residual(
                (0): Conv2dBatchAct(64, 64, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
                (1): Conv2dBatchAct(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
                (2): Conv2dBatch(64, 256, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0))
                (skip): Conv2dBatch(64, 256, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0))
                (post): ReLU(inplace=True)
              )
              (4_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
              )
              (5_residual): Residual(...)
              (6_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
                (2): Residual(...)
              )
              (7_residual): Residual(...)
              (8_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
                (2): Residual(...)
                (3): Residual(...)
                (4): Residual(...)
                (5): Residual(...)
                (6): Residual(...)
                (7): Residual(...)
                (8): Residual(...)
                (9): Residual(...)
                (10): Residual(...)
                (11): Residual(...)
                (12): Residual(...)
                (13): Residual(...)
                (14): Residual(...)
                (15): Residual(...)
                (16): Residual(...)
                (17): Residual(...)
                (18): Residual(...)
                (19): Residual(...)
                (20): Residual(...)
                (21): Residual(...)
              )
              (9_residual): Residual(...)
              (10_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
              )
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 2048, 20, 20])
        """
        groups = (2, 3, 22, 2)
        get_block1 = cls.get_bottleneck(cls.conv_type1)
        get_block2 = cls.get_bottleneck(cls.conv_type2)

        return (
            # Conv 1
            ('1_convbatch',         lnl.Conv2dBatchAct(in_channels, 64, 7, 2, 3, activation=activation)),
            ('2_max',               nn.MaxPool2d(3, 2, 1)),

            # Conv 2_x
            ('3_residual',          get_block1(64, 64, 256, 1, activation)),
            ('4_residualgroup',     nn.Sequential(*(groups[0]*[get_block1(256, 64, 256, 1, activation)]))),

            # Conv 3_x
            ('5_residual',          get_block2(256, 128, 512, 2, activation)),
            ('6_residualgroup',     nn.Sequential(*(groups[1]*[get_block2(512, 128, 512, 1, activation)]))),

            # Conv 4_x
            ('7_residual',          get_block2(512, 256, 1024, 2, activation)),
            ('8_residualgroup',     nn.Sequential(*(groups[2]*[get_block2(1024, 256, 1024, 1, activation)]))),

            # Conv 5_x
            ('9_residual',          get_block2(1024, 512, out_channels, 2, activation)),
            ('10_residualgroup',    nn.Sequential(*(groups[3]*[get_block2(out_channels, 512, out_channels, 1, activation)]))),
        )

    @BaseModule.layers(named=True, classmethod=True)
    def RN_152(
        cls,
        in_channels,
        out_channels,
        activation=default_activation,
    ):
        """
        ResNet152 backbone.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.ReLU`

        .. rubric:: Models:

        - :class:`~lightnet.models.Resnet152`

        Example:
            >>> backbone = ln.network.backbone.Resnet.RN_50(3, 2048)
            >>> print(backbone)     # doctest: +SKIP
            Sequential(
              (1_convbatch): Conv2dBatchAct(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), ReLU(inplace=True))
              (2_max): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
              (3_residual): Residual(
                (0): Conv2dBatchAct(64, 64, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
                (1): Conv2dBatchAct(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
                (2): Conv2dBatch(64, 256, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0))
                (skip): Conv2dBatch(64, 256, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0))
                (post): ReLU(inplace=True)
              )
              (4_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
              )
              (5_residual): Residual(...)
              (6_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
                (2): Residual(...)
                (3): Residual(...)
                (4): Residual(...)
                (5): Residual(...)
                (6): Residual(...)
              )
              (7_residual): Residual(...)
              (8_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
                (2): Residual(...)
                (3): Residual(...)
                (4): Residual(...)
                (5): Residual(...)
                (6): Residual(...)
                (7): Residual(...)
                (8): Residual(...)
                (9): Residual(...)
                (10): Residual(...)
                (11): Residual(...)
                (12): Residual(...)
                (13): Residual(...)
                (14): Residual(...)
                (15): Residual(...)
                (16): Residual(...)
                (17): Residual(...)
                (18): Residual(...)
                (19): Residual(...)
                (20): Residual(...)
                (21): Residual(...)
                (22): Residual(...)
                (23): Residual(...)
                (24): Residual(...)
                (25): Residual(...)
                (26): Residual(...)
                (27): Residual(...)
                (28): Residual(...)
                (29): Residual(...)
                (30): Residual(...)
                (31): Residual(...)
                (32): Residual(...)
                (33): Residual(...)
                (34): Residual(...)
              )
              (9_residual): Residual(...)
              (10_residualgroup): Sequential(
                (0): Residual(...)
                (1): Residual(...)
              )
            )
            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 2048, 20, 20])
        """
        groups = (2, 7, 35, 2)
        get_block1 = cls.get_bottleneck(cls.conv_type1)
        get_block2 = cls.get_bottleneck(cls.conv_type2)

        return (
            # Conv 1
            ('1_convbatch',         lnl.Conv2dBatchAct(in_channels, 64, 7, 2, 3, activation=activation)),
            ('2_max',               nn.MaxPool2d(3, 2, 1)),

            # Conv 2_x
            ('3_residual',          get_block1(64, 64, 256, 1, activation)),
            ('4_residualgroup',     nn.Sequential(*(groups[0]*[get_block1(256, 64, 256, 1, activation)]))),

            # Conv 3_x
            ('5_residual',          get_block2(256, 128, 512, 2, activation)),
            ('6_residualgroup',     nn.Sequential(*(groups[1]*[get_block2(512, 128, 512, 1, activation)]))),

            # Conv 4_x
            ('7_residual',          get_block2(512, 256, 1024, 2, activation)),
            ('8_residualgroup',     nn.Sequential(*(groups[2]*[get_block2(1024, 256, 1024, 1, activation)]))),

            # Conv 5_x
            ('9_residual',          get_block2(1024, 512, out_channels, 2, activation)),
            ('10_residualgroup',    nn.Sequential(*(groups[3]*[get_block2(out_channels, 512, out_channels, 1, activation)]))),
        )


class DeformableResnet(Resnet):
    """
    Resnet Backbone with deformable convolutions. |br|
    The 3x3 convolutions in the blocks C3-C5 (original resnet naming) are replaced by deformable convolutions,
    as explained in :cite:`deformable_conv2`.
    """
    conv_type1 = nn.Conv2d
    conv_type2 = lnl.DeformableConv2d


class ModulatedResnet(Resnet):
    """
    Resnet Backbone with modulated deformable convolutions. |br|
    The 3x3 convolutions in the blocks C3-C5 (original resnet naming) are replaced by modulated deformable convolutions,
    as explained in :cite:`deformable_conv2`.
    """
    conv_type1 = nn.Conv2d
    conv_type2 = lnl.ModulatedDeformableConv2d

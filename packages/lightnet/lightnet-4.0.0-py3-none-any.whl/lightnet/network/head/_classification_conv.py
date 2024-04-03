#
#   Convolutional Classification head
#   Copyright EAVISE
#
import torch.nn as nn
from .._basemodule import BaseModule

__all__ = ['ClassificationConv']


class ClassificationConv(BaseModule):
    """ Convolutional Classification head.

    Args:
        in_channels (int): Number of input channels
        num_classes (int): Number of classes
        conv_first (bool, optional): Whether to place the convolution before or after the :class:`~torch.nn.AdaptiveAvgPool2d`; Default **False**
        dropout (float, optional): Dropout probability (set to zero to disable); Default **0**
        activation (nn.Module, optional): Activation function to add after the convolution; Default **None**

    .. rubric:: Models:

    - :class:`~lightnet.models.Darknet`
    - :class:`~lightnet.models.Darknet19`
    - :class:`~lightnet.models.Darknet53`
    - :class:`~lightnet.models.MobilenetV1`
    - :class:`~lightnet.models.MobilenetV2`
    - :class:`~lightnet.models.MobileDarknet19`

    Examples:
        >>> head = ln.network.head.ClassificationConv(1024, 1000)
        >>> print(head)
        Sequential(
          (0): AdaptiveAvgPool2d(output_size=1)
          (1): Conv2d(1024, 1000, kernel_size=(1, 1), stride=(1, 1))
          (2): Flatten(start_dim=1, end_dim=-1)
        )
        >>> in_tensor = torch.rand(1, 1024, 13, 13)
        >>> out_tensor = head(in_tensor)
        >>> print(out_tensor.shape)
        torch.Size([1, 1000])
    """
    @BaseModule.layers
    def Default(
        in_channels,
        num_classes,
        conv_first=False,
        dropout=0,
        activation=None,
    ):
        conv_layers = [
            nn.Conv2d(in_channels, num_classes, 1, 1, 0),
        ]

        if dropout > 0:
            conv_layers.insert(0, nn.Dropout(p=dropout))
        if activation is not None:
            conv_layers.append(activation)

        if conv_first:
            return (
                *conv_layers,
                nn.AdaptiveAvgPool2d(1),
                nn.Flatten(),
            )
        else:
            return (
                nn.AdaptiveAvgPool2d(1),
                *conv_layers,
                nn.Flatten(),
            )

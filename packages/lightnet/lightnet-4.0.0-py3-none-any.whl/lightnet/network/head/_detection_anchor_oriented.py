#
#   Oriented Yolo detection head
#   Copyright EAVISE
#
from functools import partial
import torch.nn as nn
from .. import layer as lnl
from .._basemodule import BaseModule

__all__ = ['DetectionOrientedAnchor']


class DetectionOrientedAnchor(BaseModule):
    """ Oriented Anchor Detection head. |br|
    This head adds an extra rotation angle to each predicted bounding box.

    Args:
        in_channels (int): Number of input channels
        num_anchors (int): Number of anchors
        num_classes (int): Number of classes
        inter_channels (int, optional): How many channels to use for the intermediate convolution; Default **1024**
        point_wise (bool, optional): Whether to use a 1x1 pointwise or a regular 3x3 intermediate convolution; Default **False**
        momentum (float, optional): Momentum of the moving averages of the normalization; Default **0.01**
        activation (class, optional): Which activation function to use; Default :class:`torch.nn.LeakyReLU(0.1)`

    .. rubric:: Models:

    - :class:`~lightnet.models.O_DYolo`
    - :class:`~lightnet.models.O_YoloV2`
    - :class:`~lightnet.models.O_YoloV3`
    - :class:`~lightnet.models.O_Yolt`

    Examples:
        >>> head = ln.network.head.DetectionOrientedAnchor(1280, 5, 20)
        >>> print(head)
        Sequential(
          (0): Conv2dBatchAct(1280, 1024, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), LeakyReLU(negative_slope=0.1, inplace=True))
          (1): Conv2d(1024, 130, kernel_size=(1, 1), stride=(1, 1))
        )
        >>> in_tensor = torch.rand(1, 1280, 13, 13)
        >>> out_tensor = head(in_tensor)
        >>> print(out_tensor.shape)
        torch.Size([1, 130, 13, 13])
    """
    default_activation = partial(nn.LeakyReLU, 0.1, inplace=True)

    @BaseModule.layers
    def Default(
        in_channels,
        num_anchors,
        num_classes,
        inter_channels=1024,
        point_wise=False,
        momentum=0.01,
        activation=default_activation,
    ):
        kernel = (1, 1, 0) if point_wise else (3, 1, 1)
        return (
            lnl.Conv2dBatchAct(in_channels, inter_channels, *kernel, activation=activation, momentum=momentum),
            nn.Conv2d(inter_channels, num_anchors*(6+num_classes), 1, 1, 0),
        )

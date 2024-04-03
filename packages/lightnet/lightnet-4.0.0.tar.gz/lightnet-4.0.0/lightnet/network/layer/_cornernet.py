#
#   Cornernet pooling layers
#   Copyright EAVISE
#
from functools import partial
from collections import OrderedDict
import torch.nn as nn
from ._conv import Conv2dBatch, Conv2dBatchAct
from ._util import ParallelSum

__all__ = ['TopPool', 'BottomPool', 'LeftPool', 'RightPool', 'CornerPool']


class TopPool(nn.Module):
    """ Top pooling implementation :cite:`cornernet`. |br|
    This layer is not a traditional pooling layer in the sence that it does not modify the dimension of the input tensor.

    .. figure:: /.static/api/toppool.*
       :width: 100%
       :alt: TopPool module design

    Example:
        >>> module = ln.network.layer.TopPool()
        >>> in_tensor = torch.rand(1, 3, 10, 10)
        >>> out_tensor = module(in_tensor)
        >>> out_tensor.shape
        torch.Size([1, 3, 10, 10])
    """
    def forward(self, x):
        return x.flip(2).cummax(2)[0].flip(2)


class BottomPool(nn.Module):
    """ Bottom pooling implementation :cite:`cornernet`. |br|
    This layer is not a traditional pooling layer in the sence that it does not modify the dimension of the input tensor.

    .. figure:: /.static/api/bottompool.*
       :width: 100%
       :alt: BottomPool module design

    Example:
        >>> module = ln.network.layer.BottomPool()
        >>> in_tensor = torch.rand(1, 3, 10, 10)
        >>> out_tensor = module(in_tensor)
        >>> out_tensor.shape
        torch.Size([1, 3, 10, 10])
    """
    def forward(self, x):
        return x.cummax(2)[0]


class LeftPool(nn.Module):
    """ Left pooling implementation :cite:`cornernet`. |br|
    This layer is not a traditional pooling layer in the sence that it does not modify the dimension of the input tensor.

    .. figure:: /.static/api/leftpool.*
       :width: 100%
       :alt: LeftPool module design

    Example:
        >>> module = ln.network.layer.LeftPool()
        >>> in_tensor = torch.rand(1, 3, 10, 10)
        >>> out_tensor = module(in_tensor)
        >>> out_tensor.shape
        torch.Size([1, 3, 10, 10])
    """
    def forward(self, x):
        return x.flip(3).cummax(3)[0].flip(3)


class RightPool(nn.Module):
    """ Right pooling implementation :cite:`cornernet`. |br|
    This layer is not a traditional pooling layer in the sence that it does not modify the dimension of the input tensor.

    .. figure:: /.static/api/rightpool.*
       :width: 100%
       :alt: RightPool module design

    Example:
        >>> module = ln.network.layer.RightPool()
        >>> in_tensor = torch.rand(1, 3, 10, 10)
        >>> out_tensor = module(in_tensor)
        >>> out_tensor.shape
        torch.Size([1, 3, 10, 10])
    """
    def forward(self, x):
        return x.cummax(3)[0]


class CornerPool(nn.Module):
    """ Cornerpooling module implementation :cite:`cornernet`.

    Args:
        channels (int): Number of input and output channels
        pool1 (nn.Module): First pooling module
        pool2 (nn.Module): Second pooling module
        inter_channels (int, optional): Intermediate channels; Default **128**
        momentum (number, optional): momentum of the moving averages of the normalization; Default **0.1**
        relu (class, optional): Which ReLU to use; Default :class:`torch.nn.ReLU`

    .. figure:: /.static/api/cornerpool.*
       :width: 100%
       :alt: CornerPool module design

    Example:
        >>> module = ln.network.layer.CornerPool(32, ln.network.layer.TopPool, ln.network.layer.BottomPool)
        >>> print(module)
        CornerPool(32, TopPool, BottomPool, inter_channels=128, ReLU(inplace=True))
        >>> in_tensor = torch.rand(1, 32, 10, 10)
        >>> out_tensor = module(in_tensor)
        >>> out_tensor.shape
        torch.Size([1, 32, 10, 10])

    Warning:
        Compared to the `official CornerNet implementation <cornernetImpl_>`_,
        this version of cornerpooling does not add the last 3x3 Conv2dBatchAct module.

    .. deprecated:: 4.0.0
        |br| The `relu` argument is deprecated in favor for the more generic name "activation".

    .. _cornernetImpl: https://github.com/princeton-vl/CornerNet-Lite/blob/6a54505d830a9d6afe26e99f0864b5d06d0bbbaf/core/models/py_utils/utils.py#L187
    """
    default_activation = partial(nn.ReLU, inplace=True)

    def __init__(self, channels, pool1, pool2, inter_channels=128, momentum=0.1, activation=default_activation, relu=None):
        super().__init__()

        if relu is not None:
            import warnings
            warnings.warn(
                'The "relu" argument is deprecated in favor for the more generic name "activation"',
                category=DeprecationWarning,
                stacklevel=2,
            )
            activation = relu

        self.layers = ParallelSum(OrderedDict([
            ('pool', ParallelSum(
                nn.Sequential(
                    Conv2dBatchAct(channels, inter_channels, 3, 1, 1, activation=activation, momentum=momentum),
                    pool1(),
                ),
                nn.Sequential(
                    Conv2dBatchAct(channels, inter_channels, 3, 1, 1, activation=activation, momentum=momentum),
                    pool2(),
                ),
                post=Conv2dBatch(inter_channels, channels, 3, 1, 1),
            )),
            ('conv', Conv2dBatch(channels, channels, 1, 1, 0)),
            ('post', activation()),
        ]))

    def __repr__(self):
        s = '{name}({channels}, {pool1}, {pool2}, inter_channels={inter_channels}, {activation})'
        return s.format(
            name=self.__class__.__name__,
            channels=self.layers.pool[0][0].layers[0].in_channels,
            pool1=self.layers.pool[0][1].__class__.__name__,
            pool2=self.layers.pool[1][1].__class__.__name__,
            inter_channels=self.layers.pool[0][0].layers[0].out_channels,
            activation=self.layers.post,
        )

    def forward(self, x):
        return self.layers(x)

    @property
    def in_channels(self):
        return self.layers.pool[0][0].layers[0].in_channels

    @property
    def out_channels(self):
        return self.layers.conv[0].out_channels

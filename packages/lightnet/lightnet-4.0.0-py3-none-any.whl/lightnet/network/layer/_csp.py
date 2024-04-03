#
#   Cross Stage Partial Network layers
#   Copyright EAVISE
#
import torch
import torch.nn as nn


__all__ = ['CSP']


class CSP(nn.Sequential):
    """
    CSP block implementation from :cite:`cspnet`. |br|
    This module first splits the input using `split1` and `split2` provided blocks.
    Only the output of `split2` will be processed by the modules passed onto this Sequential.
    Finally, the output of both splits gets concatenated and run through the `post` module.

    Args:
        *args: Arguments passed to :class:`torch.nn.Sequential`
        split1 (nn.Module, optional): Module that is used to get the first split tensor; Default :class:`torch.nn.Identity`
        split2 (nn.Module, optional): Module that is used to get the second split tensor; Default :class:`torch.nn.Identity`
        post (nn.Module, optional): Extra module that is run on the output after everything is added; Default :class:`torch.nn.Identity`

    .. figure:: /.static/api/csp.*
       :width: 100%
       :alt: CSP module design

    Note:
        If you are using an OrderedDict to pass the modules to the sequential,
        you can set the `split1`, `split2` and `post` values inside of that dict as well.

    Example:
        >>> module = ln.network.layer.CSP(
        ...     ln.network.layer.Conv2dBatchAct(32, 32, 3, 1, 1),
        ...     ln.network.layer.Conv2dBatchAct(32, 32, 3, 1, 1),
        ...     # The split blocks are used to get the different split subtensors
        ...     split1=ln.network.layer.Conv2dBatchAct(32, 32, 1, 1, 0),
        ...     split2=ln.network.layer.Conv2dBatchAct(32, 32, 1, 1, 0),
        ...     # The post block should run on the concatenated subtensors,
        ...     # so the in_channels are equal to the sum of the out_channels of both subtensors
        ...     post=ln.network.layer.Conv2dBatchAct(64, 64, 1, 1, 0)
        ... )
        >>> print(module)
        CSP(
          (0): Conv2dBatchAct(32, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
          (1): Conv2dBatchAct(32, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
          (split1): Conv2dBatchAct(32, 32, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
          (split2): Conv2dBatchAct(32, 32, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
          (post): Conv2dBatchAct(64, 64, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
        )
        >>> in_tensor = torch.rand(1, 32, 10, 10)
        >>> out_tensor = module(in_tensor)
        >>> out_tensor.shape
        torch.Size([1, 64, 10, 10])

        It might be easier to specify the sequential with an ordered dictionary, as it allows you to order the modules in a more logical way.

        >>> from collections import OrderedDict
        >>> module = ln.network.layer.CSP(OrderedDict(
        ...     # The split blocks are used to get the different split subtensors
        ...     split1=ln.network.layer.Conv2dBatchAct(32, 32, 1, 1, 0),
        ...     split2=ln.network.layer.Conv2dBatchAct(32, 32, 1, 1, 0),
        ...     # Main modules for split2
        ...     m0=ln.network.layer.Conv2dBatchAct(32, 32, 3, 1, 1),
        ...     m1=ln.network.layer.Conv2dBatchAct(32, 32, 3, 1, 1),
        ...     # The post block that runs on the concatenated output tensor
        ...     post=ln.network.layer.Conv2dBatchAct(64, 64, 1, 1, 0)
        ... ))
        >>> print(module)
        CSP(
          (split1): Conv2dBatchAct(32, 32, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
          (split2): Conv2dBatchAct(32, 32, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
          (m0): Conv2dBatchAct(32, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
          (m1): Conv2dBatchAct(32, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), ReLU(inplace=True))
          (post): Conv2dBatchAct(64, 64, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), ReLU(inplace=True))
        )
        >>> in_tensor = torch.rand(1, 32, 10, 10)
        >>> out_tensor = module(in_tensor)
        >>> out_tensor.shape
        torch.Size([1, 64, 10, 10])
    """
    def __init__(self, *args, split1=None, split2=None, post=None):
        super().__init__(*args)

        self.split1 = split1 if split1 is not None else self._modules.get('split1', nn.Identity())
        self.split2 = split2 if split2 is not None else self._modules.get('split2', nn.Identity())
        self.post = post if post is not None else self._modules.get('post', nn.Identity())

    def forward(self, x):
        x1 = self.split1(x)
        x2 = self.split2(x)

        for name, module in self.named_children():
            if name not in ('split1', 'split2', 'post'):
                x1 = module(x1)

        y = torch.cat([x1, x2], dim=1)
        y = self.post(y)

        return y

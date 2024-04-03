#
#   Darknet Backbone
#   Copyright EAVISE
#
from collections import OrderedDict
from functools import partial
import torch.nn as nn
from .. import layer as lnl
from .._basemodule import BaseModule

__all__ = ['CSPDarknet53']


class CSPDarknet53(BaseModule):
    """ CSP Darknet backbone. """
    default_activation = partial(nn.Mish, inplace=True)

    @BaseModule.layers(named=True)
    def Default(in_channels, out_channels, momentum=0.1, activation=default_activation):
        """
        CSPDarknet53 backbone.

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            momentum (float, optional): Momentum of the moving averages of the normalization; Default **0.01**
            activation (class, optional): Which activation function to use; Default :class:`torch.nn.Mish()`

        .. rubric:: Models:

        - :class:`~lightnet.models.CSPDarknet53`

        Examples:
            >>> backbone = ln.network.backbone.CSPDarknet53(3, 1024)
            >>> print(backbone)     # doctest: +SKIP
            Sequential(
              (1_convbatch): Conv2dBatchAct(3, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), Mish(inplace=True))
              (2_convbatch): Conv2dBatchAct(32, 64, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), Mish(inplace=True))
              (3_csp): CSP(...)
              (4_convbatch): Conv2dBatchAct(128, 64, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), Mish(inplace=True))
              (5_convbatch): Conv2dBatchAct(64, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), Mish(inplace=True))
              (6_csp): CSP(...)
              (6_convbatch): Conv2dBatchAct(128, 128, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), Mish(inplace=True))
              (7_convbatch): Conv2dBatchAct(128, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), Mish(inplace=True))
              (8_csp): CSP(...)
              (9_convbatch): Conv2dBatchAct(256, 256, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), Mish(inplace=True))
              (10_convbatch): Conv2dBatchAct(256, 512, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), Mish(inplace=True))
              (11_csp): CSP(...)
              (12_convbatch): Conv2dBatchAct(512, 512, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), Mish(inplace=True))
              (13_convbatch): Conv2dBatchAct(512, 1024, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), Mish(inplace=True))
              (14_csp): CSP(...)
              (15_convbatch): Conv2dBatchAct(1024, 1024, kernel_size=(1, 1), stride=(1, 1), padding=(0, 0), Mish(inplace=True))
            )

            >>> in_tensor = torch.rand(1, 3, 640, 640)
            >>> out_tensor = backbone(in_tensor)
            >>> print(out_tensor.shape)
            torch.Size([1, 1024, 20, 20])
        """
        return (
            ('1_convbatch',         lnl.Conv2dBatchAct(in_channels, 32, 3, 1, 1, activation=activation, momentum=momentum)),
            ('2_convbatch',         lnl.Conv2dBatchAct(32, 64, 3, 2, 1, activation=activation, momentum=momentum)),
            ('3_csp',               lnl.CSP(OrderedDict([
                ('split1',          lnl.Conv2dBatchAct(64, 64, 1, 1, 0, activation=activation, momentum=momentum)),
                ('split2',          lnl.Conv2dBatchAct(64, 64, 1, 1, 0, activation=activation, momentum=momentum)),
                ('residual1',       lnl.Residual(
                                    lnl.Conv2dBatchAct(64, 32, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(32, 64, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('conv',            lnl.Conv2dBatchAct(64, 64, 1, 1, 0, activation=activation, momentum=momentum)),
                ('post',            lnl.Conv2dBatchAct(128, 64, 1, 1, 0, activation=activation, momentum=momentum)),
            ]))),
            ('4_convbatch',         lnl.Conv2dBatchAct(64, 128, 3, 2, 1, activation=activation, momentum=momentum)),
            ('5_csp',               lnl.CSP(OrderedDict([
                ('split1',          lnl.Conv2dBatchAct(128, 64, 1, 1, 0, activation=activation, momentum=momentum)),
                ('split2',          lnl.Conv2dBatchAct(128, 64, 1, 1, 0, activation=activation, momentum=momentum)),
                ('residual1',       lnl.Residual(
                                    lnl.Conv2dBatchAct(64, 64, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(64, 64, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual2',       lnl.Residual(
                                    lnl.Conv2dBatchAct(64, 64, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(64, 64, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('conv',            lnl.Conv2dBatchAct(64, 64, 1, 1, 0, activation=activation, momentum=momentum)),
                ('post',            lnl.Conv2dBatchAct(128, 128, 1, 1, 0, activation=activation, momentum=momentum)),
            ]))),
            ('6_convbatch',         lnl.Conv2dBatchAct(128, 256, 3, 2, 1, activation=activation, momentum=momentum)),
            ('7_csp',               lnl.CSP(OrderedDict([
                ('split1',          lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum)),
                ('split2',          lnl.Conv2dBatchAct(256, 128, 1, 1, 0, activation=activation, momentum=momentum)),
                ('residual1',       lnl.Residual(
                                    lnl.Conv2dBatchAct(128, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(128, 128, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual2',       lnl.Residual(
                                    lnl.Conv2dBatchAct(128, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(128, 128, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual3',       lnl.Residual(
                                    lnl.Conv2dBatchAct(128, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(128, 128, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual4',       lnl.Residual(
                                    lnl.Conv2dBatchAct(128, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(128, 128, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual5',       lnl.Residual(
                                    lnl.Conv2dBatchAct(128, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(128, 128, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual6',       lnl.Residual(
                                    lnl.Conv2dBatchAct(128, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(128, 128, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual7',       lnl.Residual(
                                    lnl.Conv2dBatchAct(128, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(128, 128, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual8',       lnl.Residual(
                                    lnl.Conv2dBatchAct(128, 128, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(128, 128, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('conv',            lnl.Conv2dBatchAct(128, 128, 1, 1, 0, activation=activation, momentum=momentum)),
                ('post',            lnl.Conv2dBatchAct(256, 256, 1, 1, 0, activation=activation, momentum=momentum)),
            ]))),
            ('8_convbatch',         lnl.Conv2dBatchAct(256, 512, 3, 2, 1, activation=activation, momentum=momentum)),
            ('9_csp',               lnl.CSP(OrderedDict([
                ('split1',          lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum)),
                ('split2',          lnl.Conv2dBatchAct(512, 256, 1, 1, 0, activation=activation, momentum=momentum)),
                ('residual1',       lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(256, 256, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual2',       lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(256, 256, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual3',       lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(256, 256, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual4',       lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(256, 256, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual5',       lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(256, 256, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual6',       lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(256, 256, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual7',       lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(256, 256, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual8',       lnl.Residual(
                                    lnl.Conv2dBatchAct(256, 256, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(256, 256, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('conv',            lnl.Conv2dBatchAct(256, 256, 1, 1, 0, activation=activation, momentum=momentum)),
                ('post',            lnl.Conv2dBatchAct(512, 512, 1, 1, 0, activation=activation, momentum=momentum)),
            ]))),
            ('10_convbatch',        lnl.Conv2dBatchAct(512, 1024, 3, 2, 1, activation=activation, momentum=momentum)),
            ('11_csp',              lnl.CSP(OrderedDict([
                ('split1',          lnl.Conv2dBatchAct(1024, 512, 1, 1, 0, activation=activation, momentum=momentum)),
                ('split2',          lnl.Conv2dBatchAct(1024, 512, 1, 1, 0, activation=activation, momentum=momentum)),
                ('residual1',       lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 512, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(512, 512, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual2',       lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 512, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(512, 512, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual3',       lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 512, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(512, 512, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('residual4',       lnl.Residual(
                                    lnl.Conv2dBatchAct(512, 512, 1, 1, 0, activation=activation, momentum=momentum),
                                    lnl.Conv2dBatchAct(512, 512, 3, 1, 1, activation=activation, momentum=momentum),
                )),
                ('conv',            lnl.Conv2dBatchAct(512, 512, 1, 1, 0, activation=activation, momentum=momentum)),
                ('post',            lnl.Conv2dBatchAct(1024, out_channels, 1, 1, 0, activation=activation, momentum=momentum)),
            ]))),
        )

#
#   CSPDarknet53 model
#   Copyright EAVISE
#
import torch.nn as nn
import lightnet.network as lnn

__all__ = ['CSPDarknet53']


class CSPDarknet53(lnn.module.Darknet):
    """ CSPDarknet53 implementation :cite:`cspnet`.

    Args:
        num_classes (int): Number of classes
        input_channels (int, optional): Number of input channels; Default **3**

    Attributes:
        self.inner_stride: Maximal internal subsampling factor of the network (input dimension should be a multiple of this)
    """
    inner_stride = 32

    # Darknet weight file module order is different than our modeling (this gets automatically applied)
    darknet_order = (
        'backbone.1_convbatch',
        'backbone.2_convbatch',
        'backbone.3_csp.split2',
        'backbone.3_csp.split1',
        'backbone.3_csp.residual1.0',
        'backbone.3_csp.residual1.1',
        'backbone.3_csp.conv',
        'backbone.3_csp.post',
        'backbone.4_convbatch',
        'backbone.5_csp.split2',
        'backbone.5_csp.split1',
        'backbone.5_csp.residual1.0',
        'backbone.5_csp.residual1.1',
        'backbone.5_csp.residual2.0',
        'backbone.5_csp.residual2.1',
        'backbone.5_csp.conv',
        'backbone.5_csp.post',
        'backbone.6_convbatch',
        'backbone.7_csp.split2',
        'backbone.7_csp.split1',
        'backbone.7_csp.residual1.0',
        'backbone.7_csp.residual1.1',
        'backbone.7_csp.residual2.0',
        'backbone.7_csp.residual2.1',
        'backbone.7_csp.residual3.0',
        'backbone.7_csp.residual3.1',
        'backbone.7_csp.residual4.0',
        'backbone.7_csp.residual4.1',
        'backbone.7_csp.residual5.0',
        'backbone.7_csp.residual5.1',
        'backbone.7_csp.residual6.0',
        'backbone.7_csp.residual6.1',
        'backbone.7_csp.residual7.0',
        'backbone.7_csp.residual7.1',
        'backbone.7_csp.residual8.0',
        'backbone.7_csp.residual8.1',
        'backbone.7_csp.conv',
        'backbone.7_csp.post',
        'backbone.8_convbatch',
        'backbone.9_csp.split2',
        'backbone.9_csp.split1',
        'backbone.9_csp.residual1.0',
        'backbone.9_csp.residual1.1',
        'backbone.9_csp.residual2.0',
        'backbone.9_csp.residual2.1',
        'backbone.9_csp.residual3.0',
        'backbone.9_csp.residual3.1',
        'backbone.9_csp.residual4.0',
        'backbone.9_csp.residual4.1',
        'backbone.9_csp.residual5.0',
        'backbone.9_csp.residual5.1',
        'backbone.9_csp.residual6.0',
        'backbone.9_csp.residual6.1',
        'backbone.9_csp.residual7.0',
        'backbone.9_csp.residual7.1',
        'backbone.9_csp.residual8.0',
        'backbone.9_csp.residual8.1',
        'backbone.9_csp.conv',
        'backbone.9_csp.post',
        'backbone.10_convbatch',
        'backbone.11_csp.split2',
        'backbone.11_csp.split1',
        'backbone.11_csp.residual1.0',
        'backbone.11_csp.residual1.1',
        'backbone.11_csp.residual2.0',
        'backbone.11_csp.residual2.1',
        'backbone.11_csp.residual3.0',
        'backbone.11_csp.residual3.1',
        'backbone.11_csp.residual4.0',
        'backbone.11_csp.residual4.1',
        'backbone.11_csp.conv',
        'backbone.11_csp.post',
        'head.1',
    )

    def __init_module__(
        self,
        num_classes,
        input_channels=3,
    ):
        self.num_classes = num_classes

        # Network
        self.backbone = lnn.backbone.CSPDarknet53(input_channels, 1024)
        self.head = lnn.head.ClassificationConv(1024, num_classes)

    def __init_weights__(self, name, mod):
        if isinstance(mod, nn.Conv2d):
            # https://github.com/digantamisra98/Mish/issues/37
            nn.init.kaiming_normal_(mod.weight, nonlinearity='leaky_relu', a=0.0003)
            if mod.bias is not None:
                nn.init.constant_(mod.bias, 0)
            return True

        return super().__init_weights__(name, mod)

    def forward(self, x):
        x = self.backbone(x)
        x = self.head(x)

        return x

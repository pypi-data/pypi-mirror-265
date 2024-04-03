#
#   ResNet models
#   Copyright EAVISE
#
import logging
from enum import Enum
import lightnet.network as lnn
import torch.nn as nn

__all__ = ['Resnet18', 'Resnet34', 'Resnet50', 'Resnet101', 'Resnet152']
log = logging.getLogger('lightnet.models')


def remap_torchvision_residual(self, k):
    if not k.startswith('layer'):
        return (
            (r'^conv1.(.*)', r'backbone.1_convbatch.layers.0.\1'),
            (r'^bn1.(.*)', r'backbone.1_convbatch.layers.1.\1'),
            (r'^fc.(.*)', r'head.2.\1'),
        )

    block_num, num, mod, remainder = k.split('.', 3)
    block_num = int(block_num[-1])
    num = int(num)

    start = (
        ('backbone.3_residual.', 'backbone.4_residualgroup.'),
        ('backbone.5_residual.', 'backbone.6_residualgroup.'),
        ('backbone.7_residual.', 'backbone.8_residualgroup.'),
        ('backbone.9_residual.', 'backbone.10_residualgroup.'),
    )[block_num - 1][int(num != 0)]
    if num != 0:
        start += f'{num-1}.'

    deformable = self.type != NetworkTypes.NORMAL and block_num >= 2
    mid = {
        'conv1': '0.layers.0.conv.' if deformable else '0.layers.0.',
        'bn1': '0.layers.1.',
        'conv2': '1.layers.0.conv.' if deformable else '1.layers.0.',
        'bn2': '1.layers.1.',
        'downsample': 'skip.layers.',
    }[mod]

    return start + mid + remainder


def remap_torchvision_bottleneck(self, k):
    if not k.startswith('layer'):
        return (
            (r'^conv1.(.*)', r'backbone.1_convbatch.layers.0.\1'),
            (r'^bn1.(.*)', r'backbone.1_convbatch.layers.1.\1'),
            (r'^fc.(.*)', r'head.2.\1'),
        )

    block_num, num, mod, remainder = k.split('.', 3)
    block_num = int(block_num[-1])
    num = int(num)

    start = (
        ('backbone.3_residual.', 'backbone.4_residualgroup.'),
        ('backbone.5_residual.', 'backbone.6_residualgroup.'),
        ('backbone.7_residual.', 'backbone.8_residualgroup.'),
        ('backbone.9_residual.', 'backbone.10_residualgroup.'),
    )[block_num - 1][int(num != 0)]
    if num != 0:
        start += f'{num-1}.'

    deformable = self.type != NetworkTypes.NORMAL and block_num >= 2
    mid = {
        'conv1': '0.layers.0.',
        'bn1': '0.layers.1.',
        'conv2': '1.layers.0.conv.' if deformable else '1.layers.0.',
        'bn2': '1.layers.1.',
        'conv3': '2.layers.0.',
        'bn3': '2.layers.1.',
        'downsample': 'skip.layers.',
    }[mod]

    return start + mid + remainder


class NetworkTypes(Enum):
    NORMAL = 0          #: Regular ResNet backbone
    DEFORMABLE = 1      #: ResNet backbone with deformable convolutions
    MODULATED = 2       #: ResNet backbone with modulated deformable convolutions

    @classmethod
    def _missing_(cls, value):
        """
        Allow instantiating enum with string values as well.
        """
        if isinstance(value, str):
            try:
                return cls[value.upper()]
            except KeyError as err:
                raise ValueError(f"'{value.upper()}' is not a valid {cls.__name__}") from err
        else:
            return super()._missing_(value)


class Resnet(lnn.module.Lightnet):
    """ Base Resnet network """
    Types = NetworkTypes
    inner_stride = 32

    def __init_module__(
        self,
        version,
        num_classes,
        input_channels=3,
        output_channels_backbone=2048,
        type=NetworkTypes.NORMAL,
    ):
        self.num_classes = num_classes
        self.input_channels = input_channels
        self.type = NetworkTypes(type)

        # Network
        if self.type == NetworkTypes.MODULATED:
            Backbone = lnn.backbone.ModulatedResnet
        elif self.type == NetworkTypes.DEFORMABLE:
            Backbone = lnn.backbone.DeformableResnet
        else:
            Backbone = lnn.backbone.Resnet

        self.backbone = getattr(Backbone, version)(input_channels, output_channels_backbone)
        self.head = lnn.head.ClassificationFC(output_channels_backbone, num_classes)

    def __init_weights__(self, name, mod):
        if name.endswith('residual.2.layers.1') or ('residualgroup' in name and name.endswith('2.layers.1')):
            nn.init.constant_(mod.weight, 0)
            nn.init.constant_(mod.bias, 0)
            return True

        return super().__init_weights__(name, mod)

    def forward(self, x):
        x = self.backbone(x)
        x = self.head(x)

        return x


class Resnet18(Resnet):
    """ ResNet18 implementation :cite:`resnet`.

    Args:
        num_classes (Number): Number of classes
        input_channels (Number, optional): Number of input channels; Default **3**
        type (enum or int, optional): Which backbone type; Default **NORMAL**

    Attributes:
        self.inner_stride: Maximal internal subsampling factor of the network (input dimension should be a multiple of this)
        self.remap_torchvision: Remapping rules for weights from the `torchvision implementation <torchvision_>`_.
        self.Types: The different backbone types (``NORMAL``, ``DEFORMABLE``, ``MODULATED``)

    Note:
        We zero-initialize the last BN in each residual branch,
        so that the residual branch starts with zeros and each residual block behaves like an identity.
        This improves the model by 0.2~0.3% according to :cite:`imagenet_1h`.

    .. _torchvision: https://pytorch.org/hub/pytorch_vision_resnet
    """
    remap_torchvision = remap_torchvision_residual

    def __init_module__(
        self,
        num_classes,
        input_channels=3,
        type=NetworkTypes.NORMAL,
    ):
        super().__init_module__(
            'RN_18',
            num_classes,
            input_channels,
            output_channels_backbone=512,
            type=type,
        )


class Resnet34(Resnet):
    """ ResNet34 implementation :cite:`resnet`.

    Args:
        num_classes (Number): Number of classes
        input_channels (Number, optional): Number of input channels; Default **3**
        type (enum or int, optional): Which backbone type; Default **NORMAL**

    Attributes:
        self.inner_stride: Maximal internal subsampling factor of the network (input dimension should be a multiple of this)
        self.remap_torchvision: Remapping rules for weights from the `torchvision implementation <torchvision_>`_.
        self.Types: The different backbone types (``NORMAL``, ``DEFORMABLE``, ``MODULATED``)

    Note:
        We zero-initialize the last BN in each residual branch,
        so that the residual branch starts with zeros and each residual block behaves like an identity.
        This improves the model by 0.2~0.3% according to :cite:`imagenet_1h`.

    .. _torchvision: https://pytorch.org/hub/pytorch_vision_resnet
    """
    remap_torchvision = remap_torchvision_residual

    def __init_module__(
        self,
        num_classes,
        input_channels=3,
        type=NetworkTypes.NORMAL,
    ):
        super().__init_module__(
            'RN_34',
            num_classes,
            input_channels,
            output_channels_backbone=512,
            type=type,
        )


class Resnet50(Resnet):
    """ ResNet50 implementation :cite:`resnet`.

    Args:
        num_classes (Number): Number of classes
        input_channels (Number, optional): Number of input channels; Default **3**
        type (enum or int, optional): Which backbone type; Default **NORMAL**

    Attributes:
        self.inner_stride: Maximal internal subsampling factor of the network (input dimension should be a multiple of this)
        self.remap_torchvision: Remapping rules for weights from the `torchvision implementation <torchvision_>`_.
        self.Types: The different backbone types (``NORMAL``, ``DEFORMABLE``, ``MODULATED``)

    Note:
        We zero-initialize the last BN in each residual branch,
        so that the residual branch starts with zeros and each residual block behaves like an identity.
        This improves the model by 0.2~0.3% according to :cite:`imagenet_1h`.

    .. _torchvision: https://pytorch.org/hub/pytorch_vision_resnet
    """
    remap_torchvision = remap_torchvision_bottleneck

    def __init_module__(
        self,
        num_classes,
        input_channels=3,
        type=NetworkTypes.NORMAL,
    ):
        super().__init_module__(
            'RN_50',
            num_classes,
            input_channels,
            type=type,
        )


class Resnet101(Resnet):
    """ ResNet101 implementation :cite:`resnet`.

    Args:
        num_classes (Number): Number of classes
        input_channels (Number, optional): Number of input channels; Default **3**
        type (enum or int, optional): Which backbone type; Default **NORMAL**

    Attributes:
        self.inner_stride: Maximal internal subsampling factor of the network (input dimension should be a multiple of this)
        self.remap_torchvision: Remapping rules for weights from the `torchvision implementation <torchvision_>`_.
        self.Types: The different backbone types (``NORMAL``, ``DEFORMABLE``, ``MODULATED``)

    Note:
        We zero-initialize the last BN in each residual branch,
        so that the residual branch starts with zeros and each residual block behaves like an identity.
        This improves the model by 0.2~0.3% according to :cite:`imagenet_1h`.

    .. _torchvision: https://pytorch.org/hub/pytorch_vision_resnet
    """
    remap_torchvision = remap_torchvision_bottleneck

    def __init_module__(
        self,
        num_classes,
        input_channels=3,
        type=NetworkTypes.NORMAL,
    ):
        super().__init_module__(
            'RN_101',
            num_classes,
            input_channels,
            type=type,
        )


class Resnet152(Resnet):
    """ ResNet152 implementation :cite:`resnet`.

    Args:
        num_classes (Number): Number of classes
        input_channels (Number, optional): Number of input channels; Default **3**
        type (enum or int, optional): Which backbone type; Default **NORMAL**

    Attributes:
        self.inner_stride: Maximal internal subsampling factor of the network (input dimension should be a multiple of this)
        self.remap_torchvision: Remapping rules for weights from the `torchvision implementation <torchvision_>`_.
        self.Types: The different backbone types (``NORMAL``, ``DEFORMABLE``, ``MODULATED``)

    Note:
        We zero-initialize the last BN in each residual branch,
        so that the residual branch starts with zeros and each residual block behaves like an identity.
        This improves the model by 0.2~0.3% according to :cite:`imagenet_1h`.

    .. _torchvision: https://pytorch.org/hub/pytorch_vision_resnet
    """
    remap_torchvision = remap_torchvision_bottleneck

    def __init_module__(
        self,
        num_classes,
        input_channels=3,
        type=NetworkTypes.NORMAL,
    ):
        super().__init_module__(
            'RN_152',
            num_classes,
            input_channels,
            type=type,
        )

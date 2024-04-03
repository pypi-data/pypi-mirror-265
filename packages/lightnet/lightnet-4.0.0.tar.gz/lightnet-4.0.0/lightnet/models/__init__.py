"""
Lightnet Models Module |br|
This module contains networks that were recreated with this library.
Take a look at the code to learn how to use this library, or just use these models if that is all you need.
"""

# Datasets
from ._dataset_brambox import *
from ._dataset_darknet import *

# Classification
from ._network_alexnet import *
from ._network_cspdarknet53 import *
from ._network_darknet import *
from ._network_darknet19 import *
from ._network_darknet53 import *
from ._network_mobilenet_v1 import *
from ._network_mobilenet_v2 import *
from ._network_resnet import *
from ._network_vgg import *

# Eavise classification
from ._network_mobile_darknet19 import *

# Yolo
from ._network_tiny_yolo_v2 import *
from ._network_tiny_yolo_v3 import *
from ._network_yolo_v2 import *
from ._network_yolo_v3 import *
from ._network_yolo_v4 import *
from ._network_yolt import *
from ._network_dyolo import *

# Eavise Yolo
from ._network_mobilenet_yolo import *
from ._network_mobile_yolo_v2 import *
from ._network_mobile_yolo_v2_upsample import *
from ._network_resnet_yolo import *
from ._network_yolo_fusion import *
from ._network_yolo_v2_upsample import *

# Cornernet
from ._network_cornernet import *
from ._network_cornernet_squeeze import *

# Yolact
from ._network_yolact import *

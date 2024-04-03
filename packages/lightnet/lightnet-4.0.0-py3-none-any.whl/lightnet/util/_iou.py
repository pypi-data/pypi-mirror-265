#
#   IoU Utilities
#   Copyright EAVISE
#
import math
from enum import Enum
import numpy as np
import torch
from ._coords import cwh_xyxy, tlwh_xyxy

__all__ = ['IoUTypes', 'iou_cwh', 'iou_tlwh', 'iou_xyxy', 'iou_wh', 'iou_bb_cwha', 'iou_bb_quad', 'iou_circle_cwha']
EPSILON = 1e-16


class IoUTypes(Enum):
    IoU = 0
    DIoU = 1
    CIoU = 2


def iou_cwh(boxes1, boxes2, *, pairwise=False, type=IoUTypes.IoU):
    """ Compute IoU between 2 tensors of boxes, when the centerpoint, width and height are given.

    Args:
        boxes1 (torch.Tensor): List of bounding boxes
        boxes2 (torch.Tensor): List of bounding boxes
        pairwise (optional, bool): Whether to compute pairwise IoU or compare every box1 with every box2; Default **False**
        ciou (optional, bool): Whether to compute the Complete IoU formula :cite:`ciou`; Default **False**

    Returns:
        if `pairwise == True`
            torch.Tensor[len(boxes), 1]: IoU values
        if `pairwise == False`
            torch.Tensor[len(boxes1), len(boxes2)]: IoU values

    Note:
        Tensor format: [[xc, yc, w, h],...]
    """
    b1 = cwh_xyxy(boxes1, False)
    b2 = cwh_xyxy(boxes2, False)

    if type == IoUTypes.IoU:
        return _iou(*b1, *b2, pairwise=pairwise)
    elif type == IoUTypes.DIoU:
        return _diou(*b1, *b2, pairwise=pairwise)
    elif type == IoUTypes.CIoU:
        return _ciou(*b1, *b2, pairwise=pairwise)


def iou_tlwh(boxes1, boxes2, *, pairwise=False, type=IoUTypes.IoU):
    """ Compute IoU between 2 tensors of boxes, when the top-left corner, width and height are given.

    Args:
        boxes1 (torch.Tensor): List of bounding boxes
        boxes2 (torch.Tensor): List of bounding boxes
        pairwise (optional, bool): Whether to compute pairwise IoU or compare every box1 with every box2; Default **False**
        ciou (optional, bool): Whether to compute the Complete IoU formula :cite:`ciou`; Default **False**

    Returns:
        if `pairwise == True`
            torch.Tensor[len(boxes), 1]: IoU values
        if `pairwise == False`
            torch.Tensor[len(boxes1), len(boxes2)]: IoU values

    Note:
        Tensor format: [[xtl, ytl, w, h],...]
    """
    b1 = tlwh_xyxy(boxes1, False)
    b2 = tlwh_xyxy(boxes2, False)

    if type == IoUTypes.IoU:
        return _iou(*b1, *b2, pairwise=pairwise)
    elif type == IoUTypes.DIoU:
        return _diou(*b1, *b2, pairwise=pairwise)
    elif type == IoUTypes.CIoU:
        return _ciou(*b1, *b2, pairwise=pairwise)


def iou_xyxy(boxes1, boxes2, *, pairwise=False, type=IoUTypes.IoU):
    """ Compute IoU between 2 tensors of boxes, when the top-left and bottom-right corner are given.

    Args:
        boxes1 (torch.Tensor): List of bounding boxes
        boxes2 (torch.Tensor): List of bounding boxes
        pairwise (optional, bool): Whether to compute pairwise IoU or compare every box1 with every box2; Default **False**
        ciou (optional, bool): Whether to compute the Complete IoU formula :cite:`ciou`; Default **False**

    Returns:
        if `pairwise == True`
            torch.Tensor[len(boxes), 1]: IoU values
        if `pairwise == False`
            torch.Tensor[len(boxes1), len(boxes2)]: IoU values

    Note:
        Tensor format: [[xtl, ytl, xbr, ybr],...]
    """
    b1 = boxes1[:, 0:1], boxes1[:, 1:2], boxes1[:, 2:3], boxes1[:, 3:4]
    b2 = boxes2[:, 0:1], boxes2[:, 1:2], boxes2[:, 2:3], boxes2[:, 3:4]

    if type == IoUTypes.IoU:
        return _iou(*b1, *b2, pairwise=pairwise)
    elif type == IoUTypes.DIoU:
        return _diou(*b1, *b2, pairwise=pairwise)
    elif type == IoUTypes.CIoU:
        return _ciou(*b1, *b2, pairwise=pairwise)


def iou_wh(boxes1, boxes2, *, pairwise=False, type=IoUTypes.IoU):
    """
    Compute IoU between 2 tensors of boxes, when only the width and height are given. |br|
    This function assumes the boxes have the same center.

    Args:
        boxes1 (torch.Tensor): List of bounding boxes
        boxes2 (torch.Tensor): List of bounding boxes
        pairwise (optional, bool): Whether to compute pairwise IoU or compare every box1 with every box2; Default **False**
        ciou (optional, bool): Whether to compute the Complete IoU formula :cite:`ciou`; Default **False**

    Returns:
        if `pairwise == True`
            torch.Tensor[len(boxes), 1]: IoU values
        if `pairwise == False`
            torch.Tensor[len(boxes1), len(boxes2)]: IoU values

    Note:
        Tensor format: [[w, h],...]
    """
    boxes1 = boxes1 / 2
    b1 = -boxes1[:, 0:1], -boxes1[:, 1:2], boxes1[:, 0:1], boxes1[:, 1:2]

    boxes2 = boxes2 / 2
    b2 = -boxes2[:, 0:1], -boxes2[:, 1:2], boxes2[:, 0:1], boxes2[:, 1:2]

    if type == IoUTypes.IoU:
        return _iou(*b1, *b2, pairwise=pairwise)
    elif type == IoUTypes.DIoU:
        return _diou(*b1, *b2, pairwise=pairwise)
    elif type == IoUTypes.CIoU:
        return _ciou(*b1, *b2, pairwise=pairwise)


def iou_bb_cwha(boxes1, boxes2, *, pairwise=False, type=IoUTypes.IoU):
    """ Compute the IoU between the enclosed horiontal bounding boxes of rotated rectangles.

    Args:
        boxes1 (torch.Tensor): List of bounding boxes
        boxes2 (torch.Tensor): List of bounding boxes
        pairwise (optional, bool): Whether to compute pairwise IoU or compare every box1 with every box2; Default **False**
        ciou (optional, bool): Whether to compute the Complete IoU formula :cite:`ciou`; Default **False**

    Returns:
        if `pairwise == True`
            torch.Tensor[len(boxes), 1]: IoU values
        if `pairwise == False`
            torch.Tensor[len(boxes1), len(boxes2)]: IoU values

    Warning:
        This function does not compute the actual IoU between the rotated rectangles,
        but approximates it as the IoU of the enclosed horizontal bounding boxes of the rectangles.

    Note:
        Tensor format: [[xc, yc, w, h, a],...]
    """
    module = torch if isinstance(boxes1, torch.Tensor) else np

    b1abs = module.abs(boxes1[:, 4:5])
    b1sin = module.sin(b1abs)
    b1cos = module.cos(b1abs)
    b1w2 = boxes1[:, 2:3] / 2
    b1h2 = boxes1[:, 3:4] / 2
    b1x1 = boxes1[:, 0:1] - b1h2 * b1sin - b1w2 * b1cos
    b1x2 = boxes1[:, 0:1] + b1h2 * b1sin + b1w2 * b1cos
    b1y1 = boxes1[:, 1:2] - b1h2 * b1cos - b1w2 * b1sin
    b1y2 = boxes1[:, 1:2] + b1h2 * b1cos + b1w2 * b1sin

    b2abs = module.abs(boxes2[:, 4:5])
    b2sin = module.sin(b2abs)
    b2cos = module.cos(b2abs)
    b2w2 = boxes2[:, 2:3] / 2
    b2h2 = boxes2[:, 3:4] / 2
    b2x1 = boxes2[:, 0:1] - b2h2 * b2sin - b2w2 * b2cos
    b2x2 = boxes2[:, 0:1] + b2h2 * b2sin + b2w2 * b2cos
    b2y1 = boxes2[:, 1:2] - b2h2 * b2cos - b2w2 * b2sin
    b2y2 = boxes2[:, 1:2] + b2h2 * b2cos + b2w2 * b2sin

    if type == IoUTypes.IoU:
        return _iou(b1x1, b1y1, b1x2, b1y2, b2x1, b2y1, b2x2, b2y2, pairwise=pairwise)
    elif type == IoUTypes.DIoU:
        return _diou(b1x1, b1y1, b1x2, b1y2, b2x1, b2y1, b2x2, b2y2, pairwise=pairwise)
    elif type == IoUTypes.CIoU:
        return _ciou(b1x1, b1y1, b1x2, b1y2, b2x1, b2y1, b2x2, b2y2, pairwise=pairwise)


def iou_bb_quad(boxes1, boxes2, *, pairwise=False, type=IoUTypes.IoU):
    """ Compute the IoU between the enclosed horiontal bounding boxes of quads.

    Args:
        boxes1 (torch.Tensor): List of bounding boxes
        boxes2 (torch.Tensor): List of bounding boxes
        pairwise (optional, bool): Whether to compute pairwise IoU or compare every box1 with every box2; Default **False**
        ciou (optional, bool): Whether to compute the Complete IoU formula :cite:`ciou`; Default **False**

    Returns:
        if `pairwise == True`
            torch.Tensor[len(boxes), 1]: IoU values
        if `pairwise == False`
            torch.Tensor[len(boxes1), len(boxes2)]: IoU values

    Warning:
        This function does not compute the actual IoU between quads,
        but approximates it as the IoU of the enclosed horizontal bounding boxes of the quads.

    Note:
        Tensor format: [[x1, y1, x2, y2, x3, y3, x4, y4],...]

        Technically, this function can be used to compute the "iou_bb" from any polygon,
        but the polygons of each boxes tensor need the same number of points.
        In order to achieve this, you could pad the tensor by duplicating points, as we simply take the min/max values.
    """
    b1x = boxes1[:, ::2]
    b1y = boxes1[:, 1::2]
    b2x = boxes2[:, ::2]
    b2y = boxes2[:, 1::2]

    if isinstance(boxes1, torch.Tensor):
        b1x1 = torch.min(b1x, axis=1, keepdim=True)[0]
        b1x2 = torch.max(b1x, axis=1, keepdim=True)[0]
        b1y1 = torch.min(b1y, axis=1, keepdim=True)[0]
        b1y2 = torch.max(b1y, axis=1, keepdim=True)[0]
        b2x1 = torch.min(b2x, axis=1, keepdim=True)[0]
        b2x2 = torch.max(b2x, axis=1, keepdim=True)[0]
        b2y1 = torch.min(b2y, axis=1, keepdim=True)[0]
        b2y2 = torch.max(b2y, axis=1, keepdim=True)[0]
    else:
        b1x1 = np.amin(b1x, axis=1, keepdims=True)
        b1x2 = np.amax(b1x, axis=1, keepdims=True)
        b1y1 = np.amin(b1y, axis=1, keepdims=True)
        b1y2 = np.amax(b1y, axis=1, keepdims=True)
        b2x1 = np.amin(b2x, axis=1, keepdims=True)
        b2x2 = np.amax(b2x, axis=1, keepdims=True)
        b2y1 = np.amin(b2y, axis=1, keepdims=True)
        b2y2 = np.amax(b2y, axis=1, keepdims=True)

    if type == IoUTypes.IoU:
        return _iou(b1x1, b1y1, b1x2, b1y2, b2x1, b2y1, b2x2, b2y2, pairwise=pairwise)
    elif type == IoUTypes.DIoU:
        return _diou(b1x1, b1y1, b1x2, b1y2, b2x1, b2y1, b2x2, b2y2, pairwise=pairwise)
    elif type == IoUTypes.CIoU:
        return _ciou(b1x1, b1y1, b1x2, b1y2, b2x1, b2y1, b2x2, b2y2, pairwise=pairwise)


def iou_circle_cwha(boxes1, boxes2):
    """ Compute the IoU of the minimum bounding circle of the rotated rectangles :cite:`ciou`.

    Args:
        boxes1 (torch.Tensor): List of bounding boxes
        boxes2 (torch.Tensor): List of bounding boxes

    Returns:
        torch.Tensor[len(boxes1) X len(boxes2)]: IoU values

    Warning:
        This function does not compute the actual IoU between the rotated rectangles,
        but approximates it as the IoU of the minimum enclosed bounding circles of the rectangles.

    Note:
        Tensor format: [[xc, yc, w, h, a],...]
    """
    module = torch if isinstance(boxes1, torch.Tensor) else np

    # Compute radii and squared radii (radius = half of the box diagonal)
    b1r2 = (boxes1[:, 2:3] ** 2 + boxes1[:, 3:4] ** 2) / 4
    b1r1 = b1r2 ** 0.5
    b2r2 = (boxes2[None, :, 2] ** 2 + boxes2[None, :, 3] ** 2) / 4
    b2r1 = b2r2 ** 0.5

    d2 = (boxes1[:, 0:1] - boxes2[None, :, 0]) ** 2 + (boxes1[:, 1:2] - boxes2[None, :, 1]) ** 2
    d1 = d2 ** 0.5

    lx = (b1r2 - b2r2 + d2) / (2 * d1)
    ly = (b1r2 - lx ** 2) ** 0.5

    intersections = b1r2 * module.arcsin(ly / b1r1) + b2r2 * module.arcsin(ly / b2r1) - ly * (lx + (b1r2 - b2r2 + lx**2) ** 0.5)
    unions = math.pi * (b1r2 + b2r2) - intersections

    return intersections / unions


def _iou(b1x1, b1y1, b1x2, b1y2, b2x1, b2y1, b2x2, b2y2, *, pairwise=False):
    """ Internal IoU function to reduce code duplication. """
    module = torch if isinstance(b1x1, torch.Tensor) else np

    if not pairwise:
        b2x1 = b2x1.T
        b2x2 = b2x2.T
        b2y1 = b2y1.T
        b2y2 = b2y2.T

    dx = (module.minimum(b1x2, b2x2) - module.maximum(b1x1, b2x1)).clip(min=0)
    dy = (module.minimum(b1y2, b2y2) - module.maximum(b1y1, b2y1)).clip(min=0)
    intersections = dx * dy

    areas1 = (b1x2 - b1x1) * (b1y2 - b1y1)
    areas2 = (b2x2 - b2x1) * (b2y2 - b2y1)
    unions = (areas1 + areas2) - intersections + EPSILON

    return intersections / unions


def _diou(b1x1, b1y1, b1x2, b1y2, b2x1, b2y1, b2x2, b2y2, *, pairwise=False):
    """ Internal Distance IoU function to reduce code duplication. """
    module = torch if isinstance(b1x1, torch.Tensor) else np

    if not pairwise:
        b2x1 = b2x1.T
        b2x2 = b2x2.T
        b2y1 = b2y1.T
        b2y2 = b2y2.T

    # IoU
    dx = (module.minimum(b1x2, b2x2) - module.maximum(b1x1, b2x1)).clip(min=0)
    dy = (module.minimum(b1y2, b2y2) - module.maximum(b1y1, b2y1)).clip(min=0)
    intersections = dx * dy

    w1, h1 = b1x2 - b1x1, b1y2 - b1y1
    w2, h2 = b2x2 - b2x1, b2y2 - b2y1
    areas1 = w1 * h1
    areas2 = w2 * h2
    unions = (areas1 + areas2) - intersections + EPSILON
    iou = intersections / unions

    # Complete IoU
    convex_w = (module.maximum(b1x2, b2x2) - module.minimum(b1x1, b2x1)).clip(min=0)
    convex_h = (module.maximum(b1y2, b2y2) - module.minimum(b1y1, b2y1)).clip(min=0)
    convex_diag_squared = convex_w ** 2 + convex_h ** 2 + EPSILON
    centerpoint_dist_squared = ((b2x1 + b2x2) - (b1x1 + b1x2)) ** 2 / 4 + ((b2y1 + b2y2) - (b1y1 + b1y2)) ** 2 / 4

    return (iou - centerpoint_dist_squared / convex_diag_squared).clip(min=-1, max=1)


def _ciou(b1x1, b1y1, b1x2, b1y2, b2x1, b2y1, b2x2, b2y2, *, pairwise=False):
    """ Internal Complete IoU function to reduce code duplication. """
    module = torch if isinstance(b1x1, torch.Tensor) else np

    if not pairwise:
        b2x1 = b2x1.T
        b2x2 = b2x2.T
        b2y1 = b2y1.T
        b2y2 = b2y2.T

    # IoU
    dx = (module.minimum(b1x2, b2x2) - module.maximum(b1x1, b2x1)).clip(min=0)
    dy = (module.minimum(b1y2, b2y2) - module.maximum(b1y1, b2y1)).clip(min=0)
    intersections = dx * dy

    w1, h1 = b1x2 - b1x1, b1y2 - b1y1
    w2, h2 = b2x2 - b2x1, b2y2 - b2y1
    areas1 = w1 * h1
    areas2 = w2 * h2
    unions = (areas1 + areas2) - intersections + EPSILON
    iou = intersections / unions

    # Complete IoU
    convex_w = (module.maximum(b1x2, b2x2) - module.minimum(b1x1, b2x1)).clip(min=0)
    convex_h = (module.maximum(b1y2, b2y2) - module.minimum(b1y1, b2y1)).clip(min=0)
    convex_diag_squared = convex_w ** 2 + convex_h ** 2 + EPSILON
    centerpoint_dist_squared = ((b2x1 + b2x2) - (b1x1 + b1x2)) ** 2 / 4 + ((b2y1 + b2y2) - (b1y1 + b1y2)) ** 2 / 4
    v = (4 / module.pi ** 2) * (module.atan(w2 / (h2 + EPSILON)) - module.atan(w1 / (h1 + EPSILON))) ** 2
    with torch.no_grad():
        alpha = v / (1 - iou + v)

    return (iou - centerpoint_dist_squared / convex_diag_squared + v * alpha).clip(min=-1, max=1)


# Alias IoUTypes so we can import only the necessary function
iou_cwh.Types = IoUTypes
iou_tlwh.Types = IoUTypes
iou_xyxy.Types = IoUTypes
iou_wh.Types = IoUTypes
iou_bb_cwha.Types = IoUTypes
iou_bb_quad.Types = IoUTypes

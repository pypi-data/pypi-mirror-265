#
#   Coordinate Utilities
#   Copyright EAVISE
#
import numpy as np
import torch

__all__ = ['cwh_xyxy', 'tlwh_xyxy', 'xyxy_cwh']


def cwh_xyxy(coords, cat=True):
    """ Transform coordinates from the (xc, yc, w, h) to the (x1, y1, x2, y2) format.

    Args:
        coords (torch.Tensor): List of bounding boxes in the CWH format.
        cat (boolean, optional): Whether to concatenate the result in one tensor or return 4 separate tensors.

    Returns:
        torch.Tensor or tuple<torch.Tensor>
    """
    xy1 = (coords[:, :2] - (coords[:, 2:4] / 2))
    xy2 = (coords[:, :2] + (coords[:, 2:4] / 2))

    if cat:
        cat = torch.concatenate if isinstance(coords, torch.Tensor) else np.concatenate
        return cat((xy1, xy2), axis=1)
    else:
        return (xy1[:, 0:1], xy1[:, 1:2], xy2[:, 0:1], xy2[:, 1:2])


def tlwh_xyxy(coords, cat=True):
    """ Transform coordinates from the (xtl, ytl, w, h) to the (x1, y1, x2, y2) format.

    Args:
        coords (torch.Tensor): List of bounding boxes in the TLWH format.
        cat (boolean, optional): Whether to concatenate the result in one tensor or return 4 separate tensors.

    Returns:
        torch.Tensor or tuple<torch.Tensor>
    """
    x1, y1 = coords[:, 0:1], coords[:, 1:2]
    xy2 = coords[:, :2] + coords[:, 2:4]

    if cat:
        cat = torch.concatenate if isinstance(coords, torch.Tensor) else np.concatenate
        return cat((x1, y1, xy2), axis=1)
    return (x1, y1, xy2[:, 0:1], xy2[:, 1:2])


def xyxy_cwh(coords, cat=True):
    """ Transform coordinates from the (x1, y1, x2, y2) to the (xc, yc, w, h) format.

    Args:
        coords (torch.Tensor): List of bounding boxes in the XYXY format.
        cat (boolean, optional): Whether to concatenate the result in one tensor or return 4 separate tensors.

    Returns:
        torch.Tensor or tuple<torch.Tensor>
    """
    xy = (coords[:, :2] + coords[:, 2:4]) / 2
    wh = coords[:, 2:4] - coords[:, :2]

    if cat:
        cat = torch.concatenate if isinstance(coords, torch.Tensor) else np.concatenate
        return cat((xy, wh), axis=1)
    else:
        return (xy[:, 0:1], xy[:, 1:2], wh[:, 0:1], wh[:, 1:2])

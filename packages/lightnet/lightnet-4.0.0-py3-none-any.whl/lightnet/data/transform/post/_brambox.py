#
#   Lightnet postprocessing in brambox
#   Copyright EAVISE
#
import logging
import numpy as np
import torch.nn as nn
import pandas as pd
from lightnet._imports import bb

__all__ = ['TensorToBrambox', 'PolygonizeMask']
log = logging.getLogger(__name__)


class TensorToBrambox(nn.Module):
    """ Converts a tensor to a list of brambox objects. |br|
    The tensor needs to be in one of the :ref`common bounding box formats <getboxes>`.

    Args:
        class_label_map (list, optional): List of class labels to transform the class id's in actual names; Default **None**
        image_map (list, optional): **DEPRECATED** List of image to transform the batch numbers in actual image names; Default **None**

    Returns:
        pandas.DataFrame:
            brambox detection dataframe where the `image` column contains the batch number (int column from 1st tensor column).

    Note:
        By default, this transformation will return the image number of the batch as the image columns.

        Previously, we used the `image_map` argument to convert that column to a proper brambox categorical.
        However, this requires carefull handling of the batch number, as this number starts from zero for each new batch.
        Additionally, this only works when looping through your dataset in the same order as the `image_map`.

        .. doctest::
            :options: +SKIP

            >>> post = ln.data.transform.TensorToBrambox(
            ...     class_label_map=['person', 'dog'],
            ...     image_map=['img1', 'img2', 'img3', 'img4', 'img5']
            ... )
            >>> processed_images = 0
            >>> detections = []
            >>> for data, annos in dataloader:
            ...     # Run network
            ...     output = network(data)
            ...     # Increase batch number
            ...     output[:, 0] += processed_images
            ...     processed_images += data.shape[0]
            ...     # Run post-processing
            ...     detections.append(post(output))
            >>> # Combine detections
            >>> detections = bb.util.concat(detections, sort=False, ignore_index=True)

        Our new methodology assumes that you correctly filtered the images of the annotations in your dataset (eg. :func:`brambox.util.select_images`).
        If that is the case, you can simply copy the data-type of your annotations to the detections.
        This works even if you shuffle the dataset and also works with :class:`~lightnet.data.transform.Compose`, by passing `image_dtype` as a keyword argument.

        .. doctest::
            :options: +SKIP

            >>> post = ln.data.transform.TensorToBrambox(class_label_map=['person', 'dog'])
            >>> detections = []
            >>> for data, annos in dataloader:
            ...     # Run network
            ...     output = network(data)
            ...     # Run post-processing
            ...     detections.append(post(output, image_dtype=annos['image'].dtype))
            >>> # Combine detections
            >>> detections = bb.util.concat(detections, sort=False, ignore_index=True)

    Note:
        Just like everything in PyTorch, this transform only works on batches of images.
        This means you need to wrap your tensor of detections in a list if you want to run this transform on a single image.

    Warning:
        If no `class_label_map` is given, this transform will simply convert the class id's to a string.
    """
    def __init__(self, class_label_map=None, image_map=None):
        super().__init__()
        self.class_label_map = class_label_map
        self.image_map = image_map
        if self.class_label_map is None:
            log.warning('No class_label_map given. The indexes will be used as class_labels.')
        if image_map is not None:
            import warnings
            warnings.warn(
                'image_map is deprecated. Check out the documentation for how to use image_dtype instead.',
                category=DeprecationWarning,
                stacklevel=2,
            )

    def forward(self, boxes, *, masks=None, image_dtype=None):
        if boxes.numel() == 0:
            df = pd.DataFrame(columns=['image', 'class_label', 'id', 'x_top_left', 'y_top_left', 'width', 'height', 'confidence'])
            df.class_label = df.class_label.astype(str)

            df.image = df.image.astype(int)
            if image_dtype is not None:
                df['image'] = pd.Categorical.from_codes(df['image'], dtype=image_dtype)
            elif self.image_map is not None:
                df['image'] = pd.Categorical.from_codes(df['image'], categories=self.image_map)

            if masks is not None:
                df['segmentation'] = None
            return df

        # Get dataframe
        boxes = boxes.clone()
        shape = boxes.shape[1]
        if shape == 8:
            df = self._transform_obb(boxes)
            cols = ['image', 'class_label', 'id', 'x_top_left', 'y_top_left', 'width', 'height', 'confidence', 'segmentation']
        else:
            df = self._transform_hbb(boxes, masks)
            cols = ['image', 'class_label', 'id', 'x_top_left', 'y_top_left', 'width', 'height', 'confidence']
            if masks is not None:
                cols += ['segmentation']

        # Set column types
        df[['image', 'class_label']] = df[['image', 'class_label']].astype(int)
        df['id'] = np.nan
        df[['x_top_left', 'y_top_left', 'width', 'height', 'confidence']] = df[['x_top_left', 'y_top_left', 'width', 'height', 'confidence']].astype(float)

        # Setup class labels
        if self.class_label_map is not None:
            df['class_label'] = df['class_label'].map(dict(enumerate(self.class_label_map)))
        else:
            df['class_label'] = df['class_label'].astype(str)

        # Setup image column
        if image_dtype is not None:
            df['image'] = pd.Categorical.from_codes(df['image'], dtype=image_dtype)
        elif self.image_map is not None:
            df['image'] = pd.Categorical.from_codes(df['image'], categories=self.image_map)

        return df[cols]

    def _transform_hbb(self, boxes, masks):
        """ [batch_num, x_c, y_c, width, height, confidence, class_id] """
        # Get width/height
        boxes[:, 1:3] -= boxes[:, 3:5] / 2

        # Create dataframe
        boxes = boxes.detach().cpu().numpy()
        df = pd.DataFrame(boxes, columns=['image', 'x_top_left', 'y_top_left', 'width', 'height', 'confidence', 'class_label'])

        # Setup segmentation
        if masks is not None:
            df['segmentation'] = list(masks.detach().cpu().numpy())

        return df

    def _transform_obb(self, boxes):
        """ [batch_num, x_c, y_c, width, height, angle, confidence, class_id] """
        # Get x_tl/y_tl
        sin = boxes[:, 5].sin()
        cos = boxes[:, 5].cos()
        w2 = boxes[:, 3] / 2
        h2 = boxes[:, 4] / 2
        boxes[:, 1] += -h2*sin - w2*cos
        boxes[:, 2] += -h2*cos + w2*sin

        # Create dataframe
        boxes = boxes.detach().cpu().numpy()
        df = pd.DataFrame(boxes, columns=['image', 'x_top_left', 'y_top_left', 'width', 'height', 'angle', 'confidence', 'class_label'])

        # Get segmentation and proper coordinates
        df = bb.util.BoundingBoxTransformer(df).get_poly(buffer=0)

        return df


class PolygonizeMask(nn.Module):
    """ Transforms pizelwise segmentation masks to PyGEOS polygons. |br|
    This function converts binary segmentation masks to polygons, using the :func:`rasterio.features.shapes` function.
    Optionally, it also simplifies the polygons afterwards, with :func:`pygeos.simplify`.

    Args:
        image_size: (int or tuple or None, optional): Target image size used to rescale the segmentation masks; Default **None**
        connectivity (4 or 8, optional): connectivity argument for :func:`rasterio.features.shapes`; Default **4**
        simplify (float, optional): The maximum allowed geometry displacement for simplification (zero to disable simplify); Default **0**
        recompute_bounds (bool, optional): Whether to recompute the HBB bounds based of the segmentation; Default False

    Note:
        If no `image_size` is given, we perform no rescaling and polygonize the segmentation masks as is.
    """
    def __init__(self, image_size=None, connectivity=4, simplify=0, recompute_bounds=False):
        global affine, pgpd, rasterio, shapely
        import affine
        import pgpd
        import rasterio.features
        import shapely.geometry

        super().__init__()

        self.image_size = (image_size, image_size) if isinstance(image_size, int) else image_size
        self.connectivity = connectivity
        self.simplify = simplify
        self.recompute_bounds = recompute_bounds

    def forward(self, boxes):
        if 'segmentation' not in boxes or str(boxes['segmentation'].dtype) == 'geos':
            return boxes
        boxes = boxes.copy()

        polys = boxes['segmentation'].apply(self._polygonize)
        boxes['segmentation'] = pgpd.GeosArray.from_shapely(polys)

        if self.simplify > 0:
            boxes['segmentation'] = boxes['segmentation'].geos.simplify(self.simplify, preserve_topology=True)

        if self.recompute_bounds:
            boxes = bb.util.BoundingBoxTransformer(boxes).get_poly(buffer=0)

        return boxes

    def _polygonize(self, mask):
        mask = mask.astype(np.uint8)

        # Get transformation matrix
        if self.image_size is not None:
            mH, mW = mask.shape
            tf = affine.Affine.scale(self.image_size[1] / mW, self.image_size[0] / mH)
        else:
            tf = affine.identity

        # Polygonize
        poly = None
        for p, value in rasterio.features.shapes(mask, connectivity=self.connectivity, transform=tf):
            if value == 0:
                continue

            p = shapely.geometry.shape(p)
            if (poly is None) or (p.area > poly.area):
                poly = p

        return poly

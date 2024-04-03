#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
import logging

import numpy as np
import pandas as pd

from brambox._imports import pgpd, pygeos
from brambox.util import BoundingBoxTransformer

from ._base import AnnotationParser, ParserType

__all__ = ['DotaParser']
log = logging.getLogger(__name__)


class DotaParser(AnnotationParser):
    """
    This parser is designed to parse the DOTA anntation format.
    This format contains one text file per image.
    Each line of the file represents one polygon and is a spaces separated list of values structured as follows:

        x1 y1 x2 y2 x3 y3 x4 y4 category difficult

    ==============  ===========
    Name            Description
    ==============  ===========
    x1 y1 -> x4 y4  bounding box vertices in clockwise order
    category        class label of the object, enclosed in quotation marks
    difficult       integer 0/1 indicating whether the annotation should be considered difficult
    ==============  ===========

    Example:
        >>> image_0000.txt
            921.0 874.0 940.0 874.0 940.0 913.0 921.0 913.0 small-vehicle 0
            638.0 935.0 694.0 935.0 694.0 962.0 638.0 962.0 large-vehicle 0
            488.0 493.0 548.0 493.0 548.0 519.0 488.0 519.0 large-vehicle 0
    """

    parser_type = ParserType.MULTI_FILE
    serialize_group = 'image'
    extension = '.txt'

    def __init__(self, precision=2):
        if pgpd is None:
            raise ImportError('The DOTA parser requires PyGEOS and pgpd to be installed!')

        super().__init__()
        self.precision = precision
        self.add_column('segmentation', pd.NA)

    def pre_serialize(self, df):
        # Get OBB as pygeos data
        df = BoundingBoxTransformer(df).get_obb_poly(buffer_poly=1)

        # Get 4 unique coordinate pairs of OBB
        coords = pygeos.get_coordinates(df['segmentation'].geos.normalize())
        coords = coords.reshape(-1, 5, 2)[:, :-1].reshape(-1, 8)
        if self.precision is not None:
            coords = coords.round(self.precision)

        # Transform to string
        df['coords'] = [' '.join(map(str, row)) for row in coords]

        # Replace ' ' by - in class_label
        df['class_label'] = df['class_label'].str.replace(' ', '-')

        return df

    def serialize(self, df):
        serialized = []
        for row in df.itertuples():
            serialized.append(f'{row.coords} {row.class_label} {int(row.difficult)}')

        return '\n'.join(serialized)

    def deserialize(self, rawdata, file_id=None):
        self.append_image(file_id)

        for line in rawdata.splitlines():
            elements = line.split()

            poly = pygeos.polygons(np.array([float(el) for el in elements[:-2]]).reshape(-1, 2))
            bounds = pygeos.bounds(poly)
            data = {
                'class_label': elements[-2],
                'x_top_left': bounds[0],
                'y_top_left': bounds[1],
                'width': bounds[2] - bounds[0],
                'height': bounds[3] - bounds[1],
                'difficult': elements[-1] == '1',
                'segmentation': poly,
            }

            self.append(file_id, **data)

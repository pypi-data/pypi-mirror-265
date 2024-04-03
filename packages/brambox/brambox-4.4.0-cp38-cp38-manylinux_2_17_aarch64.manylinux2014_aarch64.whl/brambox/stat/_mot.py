#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
#   Functions for generating Multi Object Tracking Statistics
#
import logging

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

from ..util import DualGroupByNumpy, np_col
from . import coordinates

__all__ = ['mota', 'idf1']
log = logging.getLogger(__name__)


def mota(det, anno, threshold=0.5, criteria=coordinates.iou, class_label=True, **kwargs):
    """
    Computes the MOTA score between a detection and annotation dataframe set.
    This function will match detections and annotations by computing the IoU and then look at the 'id' column to compute ID Switches.

    Args:
        det (pandas.DataFrame):
            Dataframe with detections
        anno (pandas.DataFrame):
            Dataframe with annotations
        threshold (number):
            Threshold to count a detection as true positive; Default **0.5**
        criteria (callable, optional):
            function to compute a criteria value between detection and annotation; Default :func:`brambox.stat.coordinates.iou`
        class_label (boolean, optional):
            Whether class_labels must be equal to be able to match annotations and detections; Default **True**
        **kwargs (dict, optional):
            Extra keyword arguments that are passed on to the *criteria* function

    Returns:
        Number: MOTA score between -inf and 1.

    Warning:
        The dataframes need to have an additional "frame" column which contains the numerical index of the image frame in the video.
        This allows the function to know in which order to process the images to compute ID switches.

        If your dataset comprises of multiple different videos,
        you should add an additional "video" column that allows the function to group the detections by video for the computations.

    Note:
        The detection confidence is disregarded in this function, as is most often the case.
        This is because usually you would choose a working point when deploying a detection+tracking setup. |br|
        If you do need to compute MOTA at different thresholds, you should run this function with various filtered dataframes:

        >>> det = bb.io.load(...)
        >>> anno = bb.io.load(...)
        >>> for conf in range(100, 10):
        ...     filtered_det = det[det['confidence'] >= conf / 100]
        ...     print(mota(filtered_det, anno))
    """
    assert 'frame' in det.columns, 'Detection dataframe needs to have a numerical "frame" column'
    assert 'frame' in anno.columns, 'Annotation dataframe needs to have a numerical "frame" column'

    has_video = ('video' in anno.columns and 'video' in det.columns) and (det['video'].nunique() > 1 or anno['video'].nunique() > 1)
    if has_video:
        assert set(det['video'].unique()) == set(anno['video'].unique()), 'Dataframes need to have the same videos'
    criteria = criteria_decorator(criteria)

    # Create copies
    det = det.copy()
    anno = anno.copy()

    # Convert class label to integer category
    if class_label:
        anno_cl = anno['class_label']
        det_cl = det['class_label']
        uniq, cl_keys = np.unique(np.concatenate([anno_cl, det_cl]), return_inverse=True)
        if len(uniq):
            cl_keys = np.split(cl_keys, anno_cl.shape)
            anno['class_key'] = cl_keys[0]
            det['class_key'] = cl_keys[1]
        else:
            # Only one class, so it's not necessary to perform check
            class_label = False

    # Process frame by frame
    fn, fp, ids = 0, 0, 0
    det = det.sort_values('confidence', ascending=False)
    groups = (
        DualGroupByNumpy(anno, det, 'video')
        if has_video
        else [({col: np_col(anno, col) for col in anno.columns}, {col: np_col(det, col) for col in det.columns})]
    )

    for anno_vid, det_vid in groups:
        frames = sorted({*np.unique(anno_vid['frame']), *np.unique(det_vid['frame'])})
        anno_det = {}
        for frame in frames:
            anno_frame = anno_vid['frame'] == frame
            anno_frame_id = anno_vid['id'][anno_frame]
            det_frame = det_vid['frame'] == frame
            det_frame_id = det_vid['id'][det_frame]

            # Check if empty
            if not anno_frame.any():
                fp += det_frame.sum()
                continue
            if not det_frame.any():
                fn += anno_frame.sum()
                continue

            matches = np.asarray(
                criteria(
                    {
                        'x_top_left': det_vid['x_top_left'][det_frame],
                        'y_top_left': det_vid['y_top_left'][det_frame],
                        'width': det_vid['width'][det_frame],
                        'height': det_vid['height'][det_frame],
                    },
                    {
                        'x_top_left': anno_vid['x_top_left'][anno_frame],
                        'y_top_left': anno_vid['y_top_left'][anno_frame],
                        'width': anno_vid['width'][anno_frame],
                        'height': anno_vid['height'][anno_frame],
                    },
                    **kwargs,
                )
            )
            if class_label:
                matches[det_vid['class_key'][det_frame][:, None] != anno_vid['class_key'][anno_frame][None, :]] = 0

            # Check existing pairs
            det_match, anno_match = 0, 0
            matched_det = []
            for anno_id, det_id in anno_det.items():
                if anno_id in anno_frame_id and det_id in det_frame_id:
                    anno_idx = int(np.argmax(anno_frame_id == anno_id))
                    det_idx = int(np.argmax(det_frame_id == det_id))

                    if matches[det_idx, anno_idx] >= threshold:
                        matched_det.append(det_idx)
                        det_match += 1
                        anno_match += 1
                        matches[:, anno_idx] = 0
                        matches[det_idx, :] = 0

            # Check for new matches
            for det_idx, det_id in enumerate(det_frame_id):
                if det_idx in matched_det:
                    continue

                matches_d = matches[det_idx, :]
                anno_idx = matches_d.argmax()
                if matches_d[anno_idx] >= threshold:
                    anno_id = anno_frame_id[anno_idx]

                    switch = False
                    if anno_id in anno_det:
                        del anno_det[anno_id]
                        switch = True
                    if det_id in anno_det.values():
                        del anno_det[list(anno_det.keys())[list(anno_det.values()).index(det_id)]]
                        switch = True
                    ids += switch

                    anno_det[anno_id] = det_id
                    det_match += 1
                    anno_match += 1

            fp += det_frame.sum() - det_match
            fn += anno_frame.sum() - anno_match

    # Compute MOTA
    num_gt = len(anno.index)
    return 1 - ((fn + fp + ids) / num_gt)


def idf1(det, anno, threshold=0.5, criteria=coordinates.iou, class_label=True, reuse_ids=True, **kwargs):
    """
    Computes the IDF1 score between a detection and annotation dataframe set.
    This function will match detections and annotations and then look at the 'id' column to compute the best track ID matches.

    Args:
        det (pandas.DataFrame):
            Dataframe with detections
        anno (pandas.DataFrame):
            Dataframe with annotations
        threshold (number):
            Threshold to count a detection as true positive; Default **0.5**
        criteria (callable, optional):
            Function to compute a criteria value between detection and annotation; Default :func:`brambox.stat.coordinates.iou`
        class_label (boolean, optional):
            Whether class_labels must be equal to be able to match annotations and detections; Default **True**
        reuse_ids (boolean, optional):
            Whether you can reuse ID numbers between different videos (See Note); Default **True**
        **kwargs (dict, optional):
            Extra keyword arguments that are passed on to the *criteria* function

    Returns:
        Number: IDF1 score between 0 and 1.

    Note:
        When ``reuse_ids`` is set to **True**, we consider the ID numbers of your dataframes per video individually.
        When it is set to **False**, we consider the IDs globally.
        This means that if you have an ID of zero for a track in video A and for video B, we consider them to be the same object.

    Note:
        The IDF1 metric tries to find the optimal match between detection and annotation IDs,
        such that the IDs coincide for a maximum number of frames. |br|
        As such, it is not really possible to take "ignored" annotation into consideration and they are thus regarded as regular annotations.

    Note:
        The detection confidence is disregarded in this function, as is most often the case.
        This is because usually you would choose a working point when deploying a detection+tracking setup. |br|
        If you do need to compute IDF1 at different thresholds, you should run this function with various filtered dataframes:

        >>> det = bb.io.load(...)
        >>> anno = bb.io.load(...)
        >>> for conf in range(100, 10):
        ...     filtered_det = det[det['confidence'] >= conf / 100]
        ...     print(idf1(filtered_det, anno))
    """
    if det.image.dtype.name == 'category' and anno.image.dtype.name == 'category' and set(det.image.cat.categories) != set(anno.image.cat.categories):
        log.error('Annotation and detection dataframes do not have the same image categories')
    if reuse_ids and ('video' in det.columns) != ('video' in anno.columns):
        log.error(
            'One of your dataframes has no "video" column and "reuse_ids" is set to True. '
            'Beware that this might influence the results and yield a wrong output.'
        )
    criteria = criteria_decorator(criteria)

    # Create copies
    det = det.copy()
    anno = anno.copy()

    # Convert class label to integer category
    if class_label:
        anno_cl = anno['class_label']
        det_cl = det['class_label']
        _, cl_keys = np.unique(np.concatenate([anno_cl, det_cl]), return_inverse=True)
        cl_keys = np.split(cl_keys, anno_cl.shape)
        anno['class_key'] = cl_keys[0]
        det['class_key'] = cl_keys[1]

    # Rename IDs to be strictly increasing numbers
    def rename_ids(ids):
        nonlocal current

        # This part is basically the same as `return group.replace({...})`
        # but implemented with a lookup array in NumPy as it is ~100x faster
        uniq_id = np.unique(ids).astype(int)
        id_map = np.empty(uniq_id.max() + 1, dtype=int)
        new_current = current + len(uniq_id)
        id_map[uniq_id] = np.arange(current, new_current)
        current = new_current

        return pd.Series(id_map[ids.astype(int)], index=ids.index)

    current = 0
    if reuse_ids and 'video' in det.columns and det['video'].nunique() > 1:
        det['id'] = det.groupby('video', as_index=False, group_keys=False)['id'].apply(rename_ids)
    else:
        det['id'] = rename_ids(det['id'])

    current = 0
    if reuse_ids and 'video' in anno.columns and anno['video'].nunique() > 1:
        anno['id'] = anno.groupby('video', as_index=False, group_keys=False)['id'].apply(rename_ids)
    else:
        anno['id'] = rename_ids(anno['id'])

    # Sum of Binary Overlap Matrices
    def sum_binary_overlap_matrices(a, d):
        nonlocal B, criteria, threshold, class_label, kwargs

        # Compute binary overlap
        binary_overlap = np.asarray(criteria(d, a, **kwargs)) >= threshold
        if class_label:
            binary_overlap &= d['class_key'][:, None] == a['class_key'][None, :]

        # Add overlap to result array
        B[d['id'][:, None], a['id'][None, :]] += binary_overlap

    B = np.zeros((det['id'].nunique(), anno['id'].nunique()), dtype=int)
    DualGroupByNumpy(anno, det, 'image').apply_none(sum_binary_overlap_matrices)

    # Linear Sum Assignment (Best ID match)
    rows, cols = linear_sum_assignment(B, maximize=True)
    lsa = B[rows, cols].sum()

    # IDF1
    return lsa / (0.5 * (len(det.index) + len(anno.index)))


def criteria_decorator(criteria):
    """
    The criteria function gets called with a dictionary of numpy arrays as this is faster.
    The internal Brambox coordinate functions can handle this data-type,
    but we should transform the data to pandas DataFrame for custom user functions.

    Warning:
        This function does not correctly transform the image column to a proper categorical,
        but this is usually not necessary as the items passed in here are almost always one image at a time.
    """
    if criteria.__module__ == 'brambox.stat.coordinates':
        return criteria

    def wrapper(a, b, **kwargs):
        return criteria(pd.DataFrame(a), pd.DataFrame(b), **kwargs)

    return wrapper

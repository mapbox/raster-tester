import rasterio as rio
from rasterio import warp
import numpy as np


def winding_order(boundsArr):
    '''
    returns False if CCW; True is CW
    (ie, it crosses the dateline and is inverted when unprojected)
    '''
    EPSLN = 1.0e-10
    # Add EPSLN to the first point to catch exact rectangles
    boundsArr[0] += EPSLN
    delta = np.roll(boundsArr, -1, 0) - boundsArr
    return np.sum(delta[:, 0] * delta[:, 1]) > 0


def densify(boundsArr, dens=4):
    '''
    Adds points between the bounds corners
    '''
    denseBounds = np.zeros(
        ((boundsArr.shape[0]) * dens, 2),
        dtype=boundsArr.dtype)

    denseBounds[::dens] += boundsArr
    diffs = (boundsArr - np.roll(boundsArr, -1, 0)) / float(dens)
    for i in range(1, dens):
        denseBounds[i::dens] += boundsArr - (diffs * i)

    return denseBounds


def make_bounds_array(bounds):
    return np.array([
        [bounds.left, bounds.bottom],
        [bounds.right, bounds.bottom],
        [bounds.right, bounds.top],
        [bounds.left, bounds.top]
        ])


def crosses_dateline(fpath):
    '''
    Checks if a raster crosses the dateline after unprojection to epsg 4326
    '''
    with rio.open(fpath) as src:
        denseBounds = densify(make_bounds_array(src.bounds))
        unprojectedBounds = warp.transform(
            src.crs,
            {'init': 'epsg:4326'},
            denseBounds[:, 0],
            denseBounds[:, 1])

        return winding_order(np.dstack(unprojectedBounds)[0])

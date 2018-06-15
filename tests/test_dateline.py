from raster_tester import (make_bounds_array, densify,
                           transform_bounds, winding_order)

from rasterio.coords import BoundingBox

import pytest


def test_densification_count():
    boundsArr = densify(make_bounds_array(BoundingBox(-120., 45., -115., 50.)), 8)

    assert boundsArr.shape == (32, 2)
    assert not winding_order(boundsArr)


def test_4326_crossing():
    crs = {'init': 'epsg:4326'}

    boundsArr = densify(make_bounds_array(BoundingBox(170., 45., 190., 50.)))
    assert not winding_order(boundsArr)

    transformedBounds = transform_bounds(boundsArr, crs)
    assert winding_order(transformedBounds)


def test_4326_not_crossing():
    crs = {'init': 'epsg:4326'}

    boundsArr = densify(make_bounds_array(BoundingBox(-120., 45., -115., 50.)))

    transformedBounds = transform_bounds(boundsArr, crs)
    assert not winding_order(transformedBounds)


def test_should_fail_with_bad_crs():
    crs = ""
    boundsArr = densify(make_bounds_array(BoundingBox(-120., 45., -115., 50.)))

    with pytest.raises(ValueError):
        transform_bounds(boundsArr, crs)


def test_should_fail_with_no_crs():
    crs = None
    boundsArr = densify(make_bounds_array(BoundingBox(-120., 45., -115., 50.)))

    with pytest.raises(ValueError):
        transform_bounds(boundsArr, crs)

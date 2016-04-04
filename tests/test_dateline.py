from raster_tester import make_bounds_array, densify, transform_bounds, winding_order

from rasterio.coords import BoundingBox
from rasterio.crs import from_epsg


def test_4326_crossing():
    crs = from_epsg('4326')

    boundsArr = densify(make_bounds_array(BoundingBox(170., 45., -170., 50.)))

    transformedBounds = transform_bounds(boundsArr, crs)

    assert winding_order(transformedBounds) == True


def test_4326_not_crossing():
    crs = from_epsg('4326')

    boundsArr = densify(make_bounds_array(BoundingBox(-120., 45., -115., 50.)))

    transformedBounds = transform_bounds(boundsArr, crs)

    assert winding_order(transformedBounds) == False
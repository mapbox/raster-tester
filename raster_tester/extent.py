import rasterio
from rasterio import warp


def safe_extent(sources, west=-180.0, south=-85, east=180.0, north=85):
    """
    Tests if raster source crosses the dateline
    or if it is outside of the defined limits
    defaults to lat/lon that can safely be reprojected to web mercator
    """
    with rasterio.drivers():
        for source in sources:
            with rasterio.open(source) as src:
                lowerleft = [a[0] for a in warp.transform(
                    src.crs, {'init': 'epsg:4326'},
                    [src.bounds[0]], [src.bounds[1]])]
                upperleft = [a[0] for a in warp.transform(
                    src.crs, {'init': 'epsg:4326'},
                    [src.bounds[0]], [src.bounds[3]])]
                lowerright = [a[0] for a in warp.transform(
                    src.crs, {'init': 'epsg:4326'},
                    [src.bounds[2]], [src.bounds[1]])]
                upperright = [a[0] for a in warp.transform(
                    src.crs, {'init': 'epsg:4326'},
                    [src.bounds[2]], [src.bounds[3]])]

                if lowerleft[0] > upperright[0]:
                    return (False, "{} crosses the dateline".format(source))

                for corner in [lowerleft, upperleft, lowerright, upperright]:
                    if corner[0] < west:
                        return (False, "{} is west of {}".format(source, west))
                    if corner[0] > east:
                        return (False, "{} is east of {}".format(source, east))
                    if corner[1] < south:
                        return (False, "{} is south of {}".format(source, south))
                    if corner[1] > north:
                        return (False, "{} is north of {}".format(source, north))

    return (True, "no extent issues")

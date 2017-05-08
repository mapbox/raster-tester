import raster_tester

import numpy as np


def mockobj(attributes, values):
    class Container:
        pass

    obj = Container()
    for att, val in zip(attributes, values):
        setattr(obj, att, val)
    return obj


def test_attribute_compare_ok():
    props = ['count', 'crs', 'dtypes', 'driver', 'bounds',
             'height', 'width', 'shape', 'nodatavals']
    values = [i for i in range(len(props))]
    src1 = mockobj(props, values)
    src2 = mockobj(props, values)
    compared = raster_tester.compare_properties(src1, src2, props)
    assert not compared


def test_attribute_compare_notok():
    props = ['count', 'crs', 'dtypes', 'driver', 'bounds',
             'height', 'width', 'shape', 'nodatavals']
    values = [i for i in range(len(props))]
    src1 = mockobj(props, values)
    values[3] = 0
    src2 = mockobj(props, values)
    compared = raster_tester.compare_properties(src1, src2, props)
    assert compared == [{'driver': {'src1': 3, 'src2': 0}}]


def test_array_compare():
    rRows, rCols = np.random.randint(10, 100, 2)
    testArray = np.zeros((rRows, rCols), dtype=np.uint16)
    diffcount, overthresh = raster_tester.array_compare(testArray, testArray)

    assert diffcount == 0
    assert not overthresh


def test_array_compare_one_overthresh():
    rRows, rCols = np.random.randint(10, 100, 2)
    testArray1 = np.zeros((rRows, rCols), dtype=np.uint16)
    testArray2 = np.zeros((rRows, rCols), dtype=np.uint16)

    testArray2[0][0] += 10
    diffcount, overthresh = raster_tester.array_compare(
        testArray1, testArray2, 9, 0)

    assert diffcount == 1
    assert overthresh


def test_array_compare_all_overthresh():
    rRows, rCols = np.random.randint(10, 100, 2)
    testArray1 = np.zeros((rRows, rCols), dtype=np.uint16)
    testArray2 = np.zeros((rRows, rCols), dtype=np.uint16) + 10
    diffcount, overthresh = raster_tester.array_compare(testArray1, testArray2)

    assert diffcount == testArray1.size
    assert overthresh


def test_array_compare_belowthresh():
    rRows, rCols = np.random.randint(10, 100, 2)
    testArray1 = np.zeros((rRows, rCols), dtype=np.uint8)
    testArray2 = np.zeros((rRows, rCols), dtype=np.uint8) + 10
    diffcount, overthresh = raster_tester.array_compare(
        testArray1, testArray2, 20, 20)

    assert diffcount == 0
    assert not overthresh


def test_array_compare_rand_overthresh():
    rRows, rCols = np.random.randint(10, 100, 2)
    testArray1 = np.zeros((rRows, rCols)) + 1
    testArray2 = np.zeros((rRows, rCols)) + 1

    fuzzrange = 15

    for i in range(fuzzrange):
        r, c = np.random.randint(0, min([rRows, rCols]) - 1, 2)
        testArray2[r][c] = 0
        testArray1[r][c] = 1

    diffcount, overthresh = raster_tester.array_compare(
        testArray1.astype(np.uint16), testArray2.astype(np.uint16), 0, 16)

    assert not overthresh


def test_attribute_compare_floats():
    props = ['test']
    values = [1.0]
    src1 = mockobj(props, values)
    values = [1.1]
    src2 = mockobj(props, values)
    compared = raster_tester.compare_properties(src1, src2, props)
    assert compared == [{'test': {'src1': 1.0, 'src2': 1.1}}]


def test_attribute_compare_crs():
    from rasterio.crs import CRS
    props = ['crs']
    values = [CRS({})]
    src1 = mockobj(props, values)
    values = [CRS({})]
    src2 = mockobj(props, values)
    compared = raster_tester.compare_properties(src1, src2, props)
    assert not compared


def test_attribute_compare_crs():
    from rasterio.crs import CRS
    props = ['crs']
    values = [CRS({})]
    src1 = mockobj(props, values)
    values = [CRS(init='EPSG:4326')]
    src2 = mockobj(props, values)
    compared = raster_tester.compare_properties(src1, src2, props)
    assert 'crs' in compared[0].keys()


def test_attribute_compare_bounds():
    from rasterio.coords import BoundingBox
    props = ['bounds']
    values = [BoundingBox(0, 0, 1, 1)]
    src1 = mockobj(props, values)
    values = [BoundingBox(0, 0, 2, 2)]
    src2 = mockobj(props, values)
    compared = raster_tester.compare_properties(src1, src2, props)
    assert compared == [{'bounds': {'src1': BoundingBox(left=0, bottom=0, right=1, top=1),
                                    'src2': BoundingBox(left=0, bottom=0, right=2, top=2)}}]

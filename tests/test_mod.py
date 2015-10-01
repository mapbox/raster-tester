import raster_tester

import numpy as np

class AttributeMocker:
    def __init__(self, attributes, setTo):
        for att, val in zip(attributes, setTo):
            setattr(self, att, val)
            
    def __getattribute__(self, attribute):
        return getattr(self, attribute)

def test_attribute_compare_ok():
    props = ['count', 'crs', 'dtypes', 'driver', 'bounds', 'height', 'width', 'shape', 'nodatavals']
    values = [i for i in xrange(len(props))]
    src1 = AttributeMocker(props, values)
    src2 = AttributeMocker(props, values)
    compared = raster_tester.compare_properties(src1, src2, props)
    assert not compared

def test_attribute_compare_notok():
    props = ['count', 'crs', 'dtypes', 'driver', 'bounds', 'height', 'width', 'shape', 'nodatavals']
    values = [i for i in xrange(len(props))]
    src1 = AttributeMocker(props, values)
    values[3] = 0
    src2 = AttributeMocker(props, values)
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
    diffcount, overthresh = raster_tester.array_compare(testArray1, testArray2, 9, 0)

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
    diffcount, overthresh = raster_tester.array_compare(testArray1, testArray2, 20, 20)

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

    diffcount, overthresh = raster_tester.array_compare(testArray1.astype(np.uint16), testArray2.astype(np.uint16), 0, 16)

    assert not overthresh
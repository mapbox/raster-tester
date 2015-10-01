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
    assert raster_tester.compare_bands(testArray, testArray).size == 0

def test_array_compare():
    rRows, rCols = np.random.randint(10, 100, 2)
    testArray1 = np.zeros((rRows, rCols)) + 1
    testArray2 = np.zeros((rRows, rCols)) + 1

    fuzzrange = 15

    for i in range(fuzzrange):
        r, c = np.random.randint(0, min([rRows, rCols]) - 1, 2)
        testArray2[r][c] = 0
        testArray1[r][c] = 1

    assert raster_tester.compare_bands(testArray1.astype(np.uint16), testArray2.astype(np.uint16), 16, 16).size == 0

def test_array_compare_threshchange():
    rRows, rCols = np.random.randint(10, 100, 2)
    testArray1 = np.zeros((rRows, rCols)) + 1
    testArray2 = np.zeros((rRows, rCols)) + 1

    fuzzrange = np.random.randint(1, 100, 1)[0]

    for i in range(fuzzrange):
        r, c = np.random.randint(0, min([rRows, rCols]) - 1, 2)
        testArray2[r][c] = 0
        testArray1[r][c] = 2

    assert raster_tester.compare_bands(testArray1.astype(np.uint16), testArray2.astype(np.uint16), 16, 1).size == fuzzrange
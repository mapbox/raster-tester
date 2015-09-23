#!/usr/bin/env python

import numpy as np
import rasterio as rio
import scipy.ndimage

def compare(srcpath1, srcpath2, max_px_diff, resample):
    with rio.drivers():
        src1 = rio.open(srcpath1)
        src2 = rio.open(srcpath2)

        count1 = src1.count
        count2 = src2.count

        props = ['count', 'crs', 'dtypes', 'driver', 'bounds', 'height', 'width', 'shape', 'nodatavals']

        for prop in props:
            a = src1.__getattribute__(prop)
            b = src2.__getattribute__(prop)
            assert a == b, "prop %s does not match (%s != %s)" % (prop, a, b)

        for bidx in range(1, count1 + 1):
            band1 = src1.read(bidx, masked=False).astype(np.int16)
            band1 = scipy.ndimage.zoom(band1, float(resample), order=1)
            band2 = src2.read(bidx, masked=False).astype(np.int16)
            band2 = scipy.ndimage.zoom(band2, float(resample), order=1)

            diff = np.absolute(band1 - band2)
            threshold = np.zeros(band1.shape)
            outliers = np.where(diff > 16)
            if outliers[0].size > max_px_diff:
                print outliers[0]
            assert outliers[0].size <= max_px_diff, "band %s has %d pixels which differ by > 16" % (bidx, outliers[0].size)

        src1.close()
        src2.close()
#!/usr/bin/env python

import click

import numpy as np
import rasterio as rio
from rasterio.warp import reproject, RESAMPLING
from rasterio import Affine

def affaux(up):
    return Affine(1, 0, 0, 0, -1, 0), Affine(up, 0, 0, 0, -up, 0)

def upsample_array(bidx, up, fr, to):
    upBidx = np.empty((bidx.shape[0] * up, bidx.shape[1] * up), dtype=bidx.dtype)

    reproject(
        bidx, upBidx,
        src_transform=fr,
        dst_transform=to,
        src_crs="EPSG:3857",
        dst_crs="EPSG:3857",
        resampling=RESAMPLING.bilinear)

    return upBidx

def compare_bands(band1, band2, max_px_diff=16, diffthresh=16):
    diff = np.absolute(band1 - band2)
            
    threshold = np.zeros(band1.shape)
    outliers = np.where(diff > diffthresh)

    return outliers[0]

def make_fill_array(height, width, downsample, dtype):
    return np.zeros(
        (int(height / downsample), int(width / downsample)),
        dtype
        )

def compare_properties(src1, src2, properties):
    noMatch = []
    for prop in properties:
        a = src1.__getattribute__(prop)
        b = src2.__getattribute__(prop)
        if a != b:
            noMatch.append({
                    prop: {
                        'src1': a,
                        'src2': b
                    }
                })
 
    if not len(noMatch):
        noMatch = None

    return noMatch


def compare(srcpath1, srcpath2, max_px_diff=0, upsample=1, downsample=1, compare_masked=True):
    with rio.open(srcpath1) as src1:
        with rio.open(srcpath2) as src2:

            count1 = src1.count
            count2 = src2.count
            compareAlpha = 1

            props = ['count', 'crs', 'dtypes', 'driver', 'bounds', 'height', 'width', 'shape', 'nodatavals']

            propCompare = compare_properties(src1, src2, props)

            assert not propCompare, propCompare 

            if compare_masked and src1.count == 4:
                ## create arrays for decimated reading
                masked_1 = make_fill_array(src1.height, src1.width, downsample, src1.meta['dtype'])
                masked_2 = make_fill_array(src2.height, src2.width, downsample, src2.meta['dtype'])

                src1.read(4, out=masked_1, masked=False)
                src2.read(4, out=masked_2, masked=False)
                compareAlpha = 0
                compare_bands(masked_1, masked_2, max_px_diff)

            for bidx in range(1, count1 + compareAlpha):
                # create arrays for decimated reading
                band1 = make_fill_array(src1.height, src1.width, downsample, src1.meta['dtype'])
                band2 = make_fill_array(src2.height, src2.width, downsample, src2.meta['dtype'])

                src1.read(bidx, out=band1, masked=False)
                band1 = band1.astype(np.int16)

                src2.read(bidx, out=band2, masked=False)
                band2 = band2.astype(np.int16)

                if compare_masked and src1.count == 4:
                    band1[masked_1 == 0] = 0
                    band2[masked_2 == 0] = 0

                if upsample > 1:
                    toAff, frAff = affaux(upsample)
                    band1 = upsample_array(band1, upsample, frAff, toAff)
                    band2 = upsample_array(band2, upsample, frAff, toAff)

                difference = compare_bands(band1, band2, max_px_diff)

                assert difference.size <= max_px_diff, "Band %s has %d pixels which differ by > 16" % (bidx, difference.size)

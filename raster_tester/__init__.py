#!/usr/bin/env python

import click

import numpy as np
import rasterio as rio
from rasterio.warp import reproject, RESAMPLING
from rasterio import Affine

def affaux(up):
    return Affine(1, 0, 0, 0, -1, 0), Affine(up, 0, 0, 0, -up, 0)

def upsample(bidx, up, fr, to):
    upBidx = np.empty((bidx.shape[0] * up, bidx.shape[1] * up), dtype=bidx.dtype)

    reproject(
        bidx, upBidx,
        src_transform=fr,
        dst_transform=to,
        src_crs="EPSG:3857",
        dst_crs="EPSG:3857",
        resampling=RESAMPLING.bilinear)

    return upBidx

def compare_bands(band1, band2, bidx, max_px_diff):
    diff = np.absolute(band1 - band2)
            
    threshold = np.zeros(band1.shape)
    outliers = np.where(diff > 16)
    if outliers[0].size > max_px_diff:
        click.echo(outliers[0], err=True)
    assert outliers[0].size <= max_px_diff, "band %s has %d pixels which differ by > 16" % (bidx, outliers[0].size)

def compare(srcpath1, srcpath2, max_px_diff=0, resample=1, downsample=64, compare_masked=True):
    with rio.drivers():
        src1 = rio.open(srcpath1)
        src2 = rio.open(srcpath2)

        count1 = src1.count
        count2 = src2.count
        compareAlpha = 1

        props = ['count', 'crs', 'dtypes', 'driver', 'bounds', 'height', 'width', 'shape', 'nodatavals']

        for prop in props:
            a = src1.__getattribute__(prop)
            b = src2.__getattribute__(prop)
            assert a == b, "prop %s does not match (%s != %s)" % (prop, a, b)

        if compare_masked and src1.count == 4:
            masked_1 = np.zeros((int(src1.height / downsample), int(src2.width / downsample)), src1.meta['dtype'])
            masked_2 = np.zeros((int(src2.height / downsample), int(src2.width / downsample)), src2.meta['dtype'])
            src1.read(4, out=masked_1, masked=False)
            src2.read(4, out=masked_2, masked=False)
            compareAlpha = 0
            compare_bands(masked_1, masked_2, 4, max_px_diff)

        for bidx in range(1, count1 + compareAlpha):
            band1 = np.zeros((int(src1.height / downsample), int(src1.width / downsample)), src1.meta['dtype'])
            src1.read(bidx, out=band1, masked=False)
            band1 = band1.astype(np.int16)

            band2 = np.zeros((int(src2.height / downsample), int(src2.width / downsample)), src2.meta['dtype'])
            src2.read(bidx, out=band2, masked=False)
            band2 = band2.astype(np.int16)

            if compare_masked and src1.count == 4:
                band1[masked_2 == 0] = 0
                band2[masked_2 == 0] = 0

            if resample > 1:
                toAff, frAff = affaux(resample)
                band1 = upsample(band1, resample, frAff, toAff)
                band2 = upsample(band2, resample, frAff, toAff)

            
            compare_bands(band1, band2, bidx, max_px_diff)

        src1.close()
        src2.close()
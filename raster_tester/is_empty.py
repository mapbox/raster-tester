import click, sys

import numpy as np
import rasterio as rio

def is_empty(input_path, randomize):
    with rio.open(input_path) as src:
        windows = [window for ij, window in src.block_windows()]
        if randomize:
            np.random.shuffle(windows)
        empty = True
        for window in windows:
            if np.any(src.read(4, window=window)):
                empty = False
                break
        return empty
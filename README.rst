raster-tester
=============

|Build Status|

::

     _______________        _______________
    |_|_|_|_|_|_|_|_|      |_|_|_|_|_|_|_|_|
    |_|_|_|_|_|_|_|_| HIRU |_|_|_|_|_|_|_|_|
    |_|_|_|_|_|_|_|_| DIFF |_|_|_|_|_|_|_|_|
    |_|_|_|_|_|_|_|_| FROM |_|_|_|_|_|_|_|_|
    |_|_|_|_|_|_|_|_| ===> |_|_|_|_|_|_|_|_|
    |_|_|_|_|_|_|_|_|      |_|_|_|_|_|_|_|_|

compare
-------

::

    Usage: raster-tester compare [OPTIONS] INPUT_1 INPUT_2

    Options:
      -p, --pixel-threshold INTEGER  Threshold for pixel diffs [default=0]
      -d, --downsample INTEGER       Downsample via decimated read for faster
                                     comparison, and to handle variation in
                                     compression artifacts [default=1]
      -u, --upsample INTEGER         Upsample to handle variation in compression
                                     artifacts [default=1]
      --compare-masked               Only compare masks + unmasked areas of RGBA
                                     rasters
      --no-error                     Compare in non stderr mode: echos "(OK|NOT
                                     OK) - <input_1> is (within|not within)
                                     <pixel-threshold> pixels of <input 2>"
      --debug                        Print ascii preview of errors
      --flex-mode                    Allow comparison of masked RGB + RGBA
      --help                         Show this message and exit.

.. |Build Status| image:: https://magnum.travis-ci.com/mapbox/raster-tester.svg?token=Dkq56qQtBntqTfE3yeVy
   :target: https://magnum.travis-ci.com/mapbox/raster-tester

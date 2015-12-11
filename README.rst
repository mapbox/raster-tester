raster-tester
=============

|Circle CI|

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
      --no-error                     Compare in non stderr mode: echos "(ok|not
                                     ok) - <input_1> is (within|not within)
                                     <pixel-threshold> pixels of <input 2>"
      --debug                        Print ascii preview of errors
      --flex-mode                    Allow comparison of masked RGB + RGBA
      --help                         Show this message and exit.

isempty
-------

::

    Usage: raster-tester isempty [OPTIONS] INPUT_1

    Options:
      -b, --bidx INTEGER            Bands to blob [default = 4]
      --randomize                   Iterate through windows in a psuedorandom fashion
      --help                        Show this message and exit.

.. |Circle CI| image:: https://circleci.com/gh/mapbox/raster-tester.svg?style=svg&circle-token=b160fc4bebd1e032df32fe8c4aff4bbea685701d
   :target: https://circleci.com/gh/mapbox/raster-tester

# raster-tester

```
 _______________        _______________
|_|_|_|_|_|_|_|_|      |_|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_|_| HIRU |_|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_|_| DIFF |_|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_|_| FROM |_|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_|_| ===> |_|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_|_|      |_|_|_|_|_|_|_|_|

```

## compare

```
Usage: raster-tester compare [OPTIONS] INPUT_1 INPUT_2

Options:
  -p, --pixel-threshold INTEGER  threshold for pixel diffs
  -r, --resample INTEGER         If the image is lossy, resample to handle
                                 variation in compression artifacts
  --help                         Show this message and exit.
```

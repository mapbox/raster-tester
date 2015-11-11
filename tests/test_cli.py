import os, shutil

from click.testing import CliRunner
from raster_tester.scripts.cli import cli

import rasterio as rio
import numpy as np

from rasterio import Affine

class TestingSetup:
    def __init__(self, testdir):
        self.path = testdir
        self.cleanup()
        os.mkdir(self.path)

    def cleanup(self):
        try:
            shutil.rmtree(self.path)
        except:
            pass


def make_fake(path, empty):
    crOptions = {
        'count': 4,
        'crs': {'init': u'epsg:3857'},
        'dtype': 'uint8',
        'affine': Affine(3.9999753066254073, 0.0, 19474931.8146, 0.0, -3.9999753148001806, -4794130.41405),
        'driver': u'GTiff',
        'transform': (19474931.8146, 3.9999753066254073, 0.0, -4794130.41405, 0.0, -3.9999753148001806),
        'height': 1024,
        'width': 1024,
        'nodata': None,
        'tiled': True,
        'blockxsize': 256,
        'blockysize': 256
        }
    with rio.open(path, 'w', **crOptions) as src:
        zz = np.zeros((4, 1024, 1024), dtype=np.uint8)
        if not empty:
            r, c = np.random.randint(0, 1023, 2)
            zz[3, r, c] += 1
        src.write(zz)

def test_cli_okcompare():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/expected/blobby.tif', 'tests/fixtures/notblobby.tif', '--upsample', '8', '--compare-masked', '--downsample', '64'])
    assert result.exit_code == 0

def test_cli_okcompare_bad():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/expected/blobby.tif', 'tests/fixtures/notblobby.tif', '--upsample', '8', '--downsample', '64'])
    assert result.exit_code == -1

def test_cli_okcompare_bad_no_error():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/expected/blobby.tif', 'tests/fixtures/notblobby.tif', '--upsample', '8', '--downsample', '64', '--no-error'])
    assert result.exit_code == 0
    assert result.output_bytes == 'NOT OK - Band 1 has 363 pixels that vary by more than 16\n'

def test_cli_okcompare_rgb():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/expected/blobby_rgb.tif', 'tests/fixtures/notblobby_rgb.tif', '--upsample', '8', '--compare-masked', '--downsample', '64', '--flex-mode'])
    assert result.exit_code == 0

def test_cli_okcompare_rgb_rev():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/fixtures/notblobby_rgb.tif', 'tests/expected/blobby_rgb.tif', '--upsample', '8', '--compare-masked', '--downsample', '64', '--flex-mode'])
    assert result.exit_code == 0

def test_cli_okcompare_bad_rgb():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/expected/blobby_rgb.tif', 'tests/fixtures/notblobby_rgb.tif', '--upsample', '8', '--downsample', '64', '--compare-masked'])
    assert result.exit_code == -1

def test_cli_okcompare_bad_rgb_rev():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/fixtures/notblobby_rgb.tif', 'tests/expected/blobby_rgb.tif', '--upsample', '8', '--downsample', '64', '--compare-masked'])
    assert result.exit_code == -1


def test_isempty():
    tmpdir = '/tmp/raster-tester'
    tester = TestingSetup(tmpdir)
    fakeEmpty = os.path.join(tmpdir, 'empty.tif')
    make_fake(fakeEmpty, True)
    runner = CliRunner()
    result = runner.invoke(cli, ['isempty', fakeEmpty, '--randomize'])
    assert result.exit_code == 0
    assert result.output_bytes == "%s is empty\n" % (fakeEmpty)
    tester.cleanup()

def test_isnotempty():
    tmpdir = '/tmp/raster-tester'
    tester = TestingSetup(tmpdir)
    fakeEmpty = os.path.join(tmpdir, 'notempty.tif')
    make_fake(fakeEmpty, False)
    runner = CliRunner()
    result = runner.invoke(cli, ['isempty', fakeEmpty, '--randomize'])
    assert result.exit_code == 1
    assert result.output_bytes == "%s is not empty\n" % (fakeEmpty)
    tester.cleanup()


    

from click.testing import CliRunner
from raster_tester.scripts.cli import cli

import rasterio as rio
import numpy as np

from rasterio import Affine


def make_fake(path, empty):
    crOptions = {
        'count': 4,
        'crs': {'init': u'epsg:3857'},
        'dtype': 'uint8',
        'transform': Affine(3.9999753066254073, 0.0, 19474931.8146,
                            0.0, -3.9999753148001806, -4794130.41405),
        'affine': Affine(3.9999753066254073, 0.0, 19474931.8146,
                         0.0, -3.9999753148001806, -4794130.41405),
        'driver': u'GTiff',
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
    """Shoult exit 0."""
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/expected/blobby.tif', 'tests/fixtures/notblobby.tif', '--upsample', '8', '--compare-masked', '--downsample', '64'])
    assert result.exit_code == 0


def test_cli_okcompare_bad():
    """Shoult exit 1."""
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/expected/blobby.tif', 'tests/fixtures/notblobby.tif'])
    assert result.exit_code == 1
    assert result.output == 'Error: not ok - Band 1 has 4356 pixels that vary by more than 16\n'


def test_cli_okcompare_bad_no_error():
    """Shoult exit 0: raster are different but  `--no-error` is set to True."""
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/expected/blobby.tif', 'tests/fixtures/notblobby.tif', '--no-error'])
    assert result.exit_code == 0
    assert result.output == 'not ok - Band 1 has 4356 pixels that vary by more than 16\n'


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
    assert result.exit_code == 1


def test_cli_okcompare_bad_rgb_rev():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/fixtures/notblobby_rgb.tif', 'tests/expected/blobby_rgb.tif', '--upsample', '8', '--downsample', '64', '--compare-masked'])
    assert result.exit_code == 1


def test_isempty(tmpdir):
    fakeEmpty = str(tmpdir.join('empty.tif'))
    make_fake(fakeEmpty, True)
    runner = CliRunner()
    result = runner.invoke(cli, ['isempty', fakeEmpty, '--randomize'])
    assert result.exit_code == 0
    assert result.output == "%s is empty\n" % (fakeEmpty)


def test_isnotempty(tmpdir):
    fakeEmpty = str(tmpdir.join('notempty.tif'))
    make_fake(fakeEmpty, False)
    runner = CliRunner()
    result = runner.invoke(cli, ['isempty', fakeEmpty, '--randomize'])
    assert result.exit_code == 1
    assert result.output == "Error: %s is not empty\n" % (fakeEmpty)


def test_does_not_cross_dateline():
    runner = CliRunner()
    result = runner.invoke(cli, ['crossesdateline', 'tests/fixtures/not_cross_dateline.tif'])
    assert result.exit_code == 0
    assert result.output == 'tests/fixtures/not_cross_dateline.tif does not cross dateline; exit 0\n'


def test_does_cross_dateline():
    runner = CliRunner()
    result = runner.invoke(cli, ['crossesdateline', 'tests/fixtures/crosses_dateline.tif'])
    assert result.exit_code == 1
    assert result.output == 'Error: tests/fixtures/crosses_dateline.tif crosses dateline; exit 1\n'


def test_does_not_cross_dateline_square():
    runner = CliRunner()
    result = runner.invoke(cli, ['crossesdateline', 'tests/fixtures/not_cross_dateline_square.tif'])
    assert result.exit_code == 0
    assert result.output == 'tests/fixtures/not_cross_dateline_square.tif does not cross dateline; exit 0\n'

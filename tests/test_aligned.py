
from click.testing import CliRunner

from raster_tester.scripts.cli import cli
import raster_tester


def test_cli_aligned():
    runner = CliRunner()
    result = runner.invoke(cli, ['isaligned',
                                 'tests/fixtures/notblobby.tif',
                                 'tests/fixtures/notblobby.tif'])

    assert result.exit_code == 0


def test_cli_notaligned():
    runner = CliRunner()
    result = runner.invoke(cli, ['isaligned',
                                 'tests/fixtures/notblobby.tif',
                                 'tests/fixtures/notblobby_rgb.tif'])

    assert result.exit_code == 1


def test_cli_tiled():
    runner = CliRunner()
    result = runner.invoke(cli, ['istiled',
                                 'tests/fixtures/tiled64.tif'])

    assert result.exit_code == 0


def test_cli_nottiled():
    runner = CliRunner()
    result = runner.invoke(cli, ['istiled',
                                 'tests/fixtures/nottiled.tif'])

    assert result.exit_code == 1


def test_cli_tiled_badblocks():
    runner = CliRunner()
    # With no-blocksize, just check that they are tiled
    result = runner.invoke(cli, ['istiled',
                                 '--no-blocksize',
                                 'tests/fixtures/tiled32.tif',
                                 'tests/fixtures/tiled64.tif'])

    assert result.exit_code == 0

    # With default, also check that have same block size
    result = runner.invoke(cli, ['istiled',
                                 'tests/fixtures/tiled32.tif',
                                 'tests/fixtures/tiled64.tif'])

    assert result.exit_code == 1


def test_func_aligned():
    result, msg = raster_tester.aligned(
        ['tests/fixtures/notblobby.tif', 'tests/fixtures/notblobby.tif'])
    assert result is True


def test_func_difftrans():
    result, msg = raster_tester.aligned(
        ['tests/fixtures/notblobby.tif', 'tests/fixtures/notblobby_rgb.tif'])
    assert result is False
    assert "Affine transform" in msg


def test_func_diffsize():
    result, msg = raster_tester.aligned(
        ['tests/fixtures/notblobby.tif', 'tests/fixtures/notblobby_diffsize.tif'])
    assert result is False
    assert 'different shape' in msg


def test_tiled():
    result, msg = raster_tester.tiled(['tests/fixtures/tiled64.tif'])
    assert result is True


def test_nottiled():
    result, msg = raster_tester.tiled(['tests/fixtures/nottiled.tif'])
    assert result is False
    assert 'not internally tiled' in msg


def test_tiled_diffblocks():
    result, msg = raster_tester.tiled(['tests/fixtures/tiled32.tif',
                                       'tests/fixtures/tiled64.tif'])
    assert result is False
    assert 'Blocksizes are not equal' in msg

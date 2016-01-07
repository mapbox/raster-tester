from click.testing import CliRunner
from raster_tester.scripts.cli import cli
import raster_tester


def test_notcrosses_aligned():
    runner = CliRunner()
    result = runner.invoke(cli, ['safe-extent',
                                 'tests/fixtures/notblobby.tif'])

    assert result.exit_code == 0


def test_notcrosses():
    result, msg = raster_tester.safe_extent(['tests/fixtures/notblobby.tif'])
    assert result is True

from click.testing import CliRunner
from raster_tester.scripts.cli import cli

def test_cli_okcompare():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/fixtures/blobby.tif', 'tests/fixtures/notblobby.tif', '--upsample', '8', '--compare-masked', '--downsample', '64'])
    assert result.exit_code == 0

def test_cli_okcompare_bad():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/fixtures/blobby.tif', 'tests/fixtures/notblobby.tif', '--upsample', '8', '--downsample', '64'])
    assert result.exit_code == -1
    
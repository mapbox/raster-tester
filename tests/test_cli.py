from click.testing import CliRunner
from raster_tester.scripts.cli import cli

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

def test_cli_okcompare_bad_rgb():
    runner = CliRunner()
    result = runner.invoke(cli, ['compare', 'tests/expected/blobby_rgb.tif', 'tests/fixtures/notblobby_rgb.tif', '--upsample', '8', '--downsample', '64', '--compare-masked'])
    assert result.exit_code == -1
    
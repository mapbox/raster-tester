import click

import raster_tester

@click.group()
def cli():
    pass

@click.command("compare")
@click.argument("input_1", type=click.Path(exists=True))
@click.argument("input_2", type=click.Path(exists=True))
@click.option("--pixel-threshold", "-p", type=int, default=0,
    help='threshold for pixel diffs')
@click.option("--resample", "-r", type=int, default=1,
    help='If the image is lossy, resample to handle variation in compression artifacts')
def compare(input_1, input_2, pixel_threshold, resample):
    raster_tester.compare(input_1, input_2, pixel_threshold, resample)

cli.add_command(compare)

@click.command("compare-coeff")
@click.argument("input_1", type=click.Path(exists=True))
@click.argument("input_2", type=click.Path(exists=True))
@click.option("--downsample", "-s", type=float, default=32.0,
    help='amount to downsample raster by [default == 32.0]')
@click.option("--coeff-threshold", "-t", type=float, default=0.99,
    help='threshold to compare by')
def compare_coeff(input_1, input_2, downsample, coeff_threshold):
    raster_tester.compare_coeff(input_1, input_2, downsample, coeff_threshold)

cli.add_command(compare_coeff)

if __name__ == "__main__":
    cli()
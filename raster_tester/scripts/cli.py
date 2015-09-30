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
@click.option("--downsample", "-d", type=int, default=64)
@click.option("--resample", "-r", type=int, default=1,
    help='If the image is lossy, resample to handle variation in compression artifacts')
@click.option("--compare-masked", is_flag=True)
def compare(input_1, input_2, pixel_threshold, downsample, resample, compare_masked):
    raster_tester.compare(input_1, input_2, pixel_threshold, resample, downsample, compare_masked)

cli.add_command(compare)

if __name__ == "__main__":
    cli()
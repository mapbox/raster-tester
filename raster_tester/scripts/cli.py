import click

import raster_tester

@click.group()
def cli():
    pass

@click.command("compare")
@click.argument("input_1", type=click.Path(exists=True))
@click.argument("input_2", type=click.Path(exists=True))
@click.option("--pixel-threshold", "-p", type=int, default=0)
def compare(input_1, input_2, pixel_threshold):
    raster_tester.compare(input_1, input_2, pixel_threshold)

cli.add_command(compare)

if __name__ == "__main__":
    cli()
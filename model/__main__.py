import re
import io
import json
from pathlib import Path
from typing import Generator, List, Optional, Tuple

import click
from PIL import Image

from .network import Network


def all_shapes(path: Path) -> Generator[Path, None, None]:
    for file in path.iterdir():
        if file.is_dir():
            yield file


def convert_to_shape(shape_path: Path) -> List[List[int]]:
    img = Image.open(shape_path)
    px = img.load()  # type: ignore
    return [[px[x, y] // 255 for x in range(img.width)] for y in range(img.height)]


@click.group()
def cli():
    pass


@cli.command()
@click.argument("size", type=int)
@click.argument("bias", type=int)
@click.option("-d", "--dataset", type=click.Path(exists=True), default=Path("training"))
@click.option("-r", "--input-weights-file", type=click.File("r"))
@click.option("-w", "--output-weights-file", type=click.File("w"))
def train(
    size: int,
    bias: int,
    dataset: Path,
    output_weights_file: Optional[io.TextIOWrapper] = None,
    input_weights_file: Optional[io.TextIOWrapper] = None,
) -> None:
    """Trains a model on the images in `<dataset>/rectangle` and `<dataset>/circle` folders."""
    weights = None
    if input_weights_file is not None:
        config = json.load(input_weights_file)
        weights = config.get("weights")
    network = Network(size, bias, weights)
    for shapes in zip(*map(Path.iterdir, all_shapes(dataset))):  # type: ignore
        for shape_path in shapes:
            print("Training on", str(shape_path))
            shape = convert_to_shape(shape_path)
            network.train(shape, bool("circle" in str(shape_path)))
    if output_weights_file is not None:
        json.dump(
            dict(
                weights=network.weights,
                output={
                    "circle": True,
                    "rectangle": False
                }
            ),
            output_weights_file,
        )


def is_right(guess: str):
    patt = r"/(?P<expected>.+)s/\d+\.png\sis\sa\s(?P<shape>.+)"
    match, *_ = re.findall(patt, guess)
    return len(set(map(str.lower, match))) == 1

@cli.command()
@click.argument("size", type=int)
@click.argument("bias", type=int)
@click.argument("weights_file", type=click.File("r"))
@click.argument("files", nargs=-1, type=click.Path(exists=True, dir_okay=False))
@click.option("-v", "--verbose", is_flag=True)
def test(size: int, bias: int, files: Tuple[Path, ...], weights_file: io.TextIOWrapper, verbose: bool) -> None:
    """Uses a trained model on an image and outputs the prediction."""
    config = json.load(weights_file)
    right = 0
    network = Network(size, bias, weights=config.get("weights"))
    for file in files:
        prediction = int(network.feed(convert_to_shape(file)))
        for result, i in config.get("output", {}).items():
            if prediction == i:
                guess = (str(file) + " is a " + result.capitalize())
                if is_right(guess):
                    right += 1
                if verbose:
                    click.echo(guess)
                
                break
    click.echo("-----------------------")
    click.echo(f"Accuracy Rate: {right / len(files) * 100}%")
    click.echo("-----------------------")


cli()

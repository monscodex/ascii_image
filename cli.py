#!/usr/bin/python3

import typer
from enum import Enum
from ascii_image import get_ascii_image


app = typer.Typer()

class Palette(str, Enum):
    expanded = "expanded"
    reduced = "reduced"
    block = "block"

@app.command()
def print_image(path : str, color : bool = typer.Option(True), palette_code : Palette = "expanded"):
    ascii_image = get_ascii_image(path, color, palette_code)

    print(ascii_image)

@app.command()
def convert_image(path : str, output_file_path : str, palette_code : Palette = "expanded"):
    ascii_image = get_ascii_image(path, color=False, palette_code=palette_code)

    with open(output_file_path, 'w') as f:
        f.write(ascii_image)


if __name__ == '__main__':
    app()

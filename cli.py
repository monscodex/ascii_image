#!/usr/bin/python3

import typer
from enum import Enum
from ascii_image import get_ascii_image


app = typer.Typer()

class PaletteCode(str, Enum):
    expanded = "expanded"
    standard = "standard"
    reduced = "reduced"
    block = "block"


# Fontratio option
def font_ratio_callback(value: float) -> float:
    if value < 0:
        raise typer.BadParameter("Negative fontratios are not possible")
    elif value == 0:
        raise typer.BadParameter("Null fontratios are not possible")
    
    return value

fontratio_option = typer.Option(0.5, callback=font_ratio_callback, help="The proportion between the width of the font to the height of the font. (x/y)")


@app.command()
def print_image(
        path : str,
        color : bool = typer.Option(True),
        palette_code : PaletteCode = "standard",
        palette : str = None,
        fontratio: float = fontratio_option
    ) -> None:
    palette = {'code': palette_code, 'specified': palette}

    ascii_image = get_ascii_image(path, color, palette, fontratio)

    print(ascii_image)

@app.command()
def convert_image(
        path : str,
        output_file_path : str,
        palette_code : PaletteCode = "standard",
        palette : str = None,
        fontratio: float = fontratio_option
    ) -> None:
    palette = {'code': palette_code, 'specified': palette}

    ascii_image = get_ascii_image(path, color=False, palette=palette, fontratio=fontratio)

    with open(output_file_path, 'w') as f:
        f.write(ascii_image)


if __name__ == '__main__':
    app()
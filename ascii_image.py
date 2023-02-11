#!/usr/bin/python3

import typer
from converter import print_ascii_image, write_ascii_image
from cli_option_processors import (
    PaletteCode,
    Color,
    get_palette_from_code_if_empty_palette,
    CHARACTER_COLORING_FUNCTIONS,
)

app = typer.Typer()

# Fontratio option
def font_ratio_callback(value: float) -> float:
    if value < 0:
        raise typer.BadParameter("Negative fontratios are not possible")
    elif value == 0:
        raise typer.BadParameter("Null fontratios are not possible")

    return value

fontratio_option = typer.Option(
    0.4,
    callback=font_ratio_callback,
    help="The proportion between the width of the font to the height of the font (x/y).",
)
palette_option = typer.Option(
    None,
    help="The palette of characters that is going to be used to convert each pixel into a character. The palette should be given in decreasing order of intensity ex: '#-. ' instead of ' .-#' .",
)
palette_code = typer.Option(
    "standard", help="The palette code for one of the preset palettes available."
)
random_option = typer.Option(
    False, help="Assign a random character from the palette to each pixel"
)
color_option = typer.Option(
    "full", help="The color compatibility you want to give the output"
)

reduction_factor = typer.Option(
    10.5,
    help="The number by which you want to reduce (scale down) the dimensions of the true image. Preserves proportions."
)


@app.command()
def print_image(
    path: str,
    color: Color = color_option,
    palette_code: PaletteCode = palette_code,
    palette: str = palette_option,
    random_char: bool = random_option,
    fontratio: float = fontratio_option,
) -> None:
    """Print the ASCII conversion of an image into the terminal."""
    palette = get_palette_from_code_if_empty_palette(palette, palette_code)

    character_coloring_function = CHARACTER_COLORING_FUNCTIONS[color]

    print_ascii_image(
        image_path=path,
        character_coloring_function=character_coloring_function,
        palette=palette,
        fontratio=fontratio,
        random_char=random_char,
    )


@app.command()
def convert_image(
    path: str,
    output_file_path: str,
    palette_code: PaletteCode = palette_code,
    palette: str = palette_option,
    random_char: bool = random_option,
    fontratio: float = fontratio_option,
    reduction_factor: float= reduction_factor
) -> None:
    """Save the ASCII conversion of an image into a file"""
    palette = get_palette_from_code_if_empty_palette(palette, palette_code)

    character_coloring_function = CHARACTER_COLORING_FUNCTIONS[Color("none")]

    write_ascii_image(
        image_path=path,
        output_file_path=output_file_path,
        character_coloring_function=character_coloring_function,
        palette=palette,
        random_char=random_char,
        fontratio=fontratio,
        reduction_factor=reduction_factor,
    )


if __name__ == "__main__":
    app()

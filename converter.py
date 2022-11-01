from PIL import Image, UnidentifiedImageError
from os import get_terminal_size
import random
from typing import Tuple
import sys

from PIL.Image import Image as ImageClass

from ascii_image_classes import PaletteOption, Color, PaletteCode


def get_ascii_image(
    path: str, color: Color, palette: PaletteOption, fontratio: float, random_char: bool
) -> str:
    img: ImageClass = try_open_image_if_it_exists(path)

    # Calculate image's dimensions in order to fit in the terminal without loosing its ratio
    width, height = get_displaying_dimensions(img, fontratio)
    img = img.resize((width, height))

    ascii_representation: str = get_ascii_representation(
        img, palette, color, random_char
    )

    return ascii_representation


def get_ascii_representation(
    img: ImageClass, palette_option: PaletteOption, color: Color, random_char: bool
) -> str:
    palette = get_palette_from_option(palette_option)

    pixels = img.load()
    width, height = img.size

    lines = []
    for y in range(height):
        # Append an empty string as it is converted to a new line
        lines.append("")

        text_line = get_pixel_line_converted_to_text(
            y, width, pixels, palette, color, random_char
        )
        lines.append(text_line)

    text_image = "\n".join(lines)

    return text_image


def get_pixel_line_converted_to_text(
    y: int, width: int, pixels, palette: str, color: Color, random_char: bool
) -> str:
    chars = [
        get_pixel_conversion(pixels[x, y], palette, color, random_char)
        for x in range(width)
    ]

    chars_to_string = "".join(chars)

    return chars_to_string


def get_pixel_conversion(
    pixel: Tuple[int, int, int], palette: str, color: Color, random_char: bool
) -> str:
    palette_char = get_corresponding_palette_char(pixel, palette, random_char)

    colored_char = get_colored_char(palette_char, color, pixel)

    return colored_char


def get_colored_char(char: str, color: Color, pixel: Tuple[int, int, int]) -> str:
    match color:
        case "full":
            return f"\033[38;2;{pixel[0]};{pixel[1]};{pixel[2]}m{char}"
        case "b&w":
            # The pixel is a tuple with (r, g, b) values
            grey = int(sum(pixel) / 3)
            return f"\033[38;2;{grey};{grey};{grey}m{char}"
        case "none" | _:
            return char


def get_palette_from_option(palette_option: PaletteOption) -> str:
    if palette_option.specified != None:
        return palette_option.specified

    palettes = {
        PaletteCode.extended: """ÆÑÊŒØMÉËÈÃÂWQBÅæ#NÁþEÄÀHKRŽœXgÐêqÛŠÕÔA€ßpmãâG¶øðé8ÚÜ$ëdÙýèÓÞÖåÿÒb¥FDñáZPäšÇàhû§ÝkŸ®S9žUTe6µOyxÎ¾f4õ5ôú&aü™2ùçw©Y£0VÍL±3ÏÌóC@nöòs¢u‰½¼‡zJƒ%¤Itocîrjv1lí=ïì<>i7†[¿?×}*{+()/»«•¬|!¡÷¦¯—^ª„”“~³º²–°­¹‹›;:’‘‚’˜ˆ¸…·¨´` """,
        PaletteCode.reduced: "@%#*+=-:. ",
        PaletteCode.block: chr(9608),
        PaletteCode.standard: """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`'. """,
    }

    return palettes[palette_option.code]


def get_corresponding_palette_char(
    pixel: Tuple[int, int, int], palette: str, random_char: bool
) -> str:
    if random_char:
        return random.choice(palette)

    # The pixel is a tuple with (r, g, b) values
    gray_value = sum(pixel) / 3

    # As the palette is ordered decreasingly, the more gray a pixel is the
    # closer to the start the character will be
    palette_index = (1 - (gray_value / 256)) * len(palette)
    palette_index = int(palette_index)

    palette_index -= 1 if palette_index == len(palette) else 0

    return palette[palette_index]


def get_displaying_dimensions(img: ImageClass, fontratio: float) -> tuple[int, int]:
    image_dimensions = get_image_dimensions(img, fontratio)
    terminal_dimensions = get_terminal_size()

    ratios = [
        image_d / terminal_d
        for image_d, terminal_d in zip(image_dimensions, terminal_dimensions)
    ]

    # We are calculating the possible adapted image dimensions
    # to then prefer the one that adapts to the terminal's dimensions
    supposed_image_height = int(image_dimensions[1] / ratios[0])
    supposed_image_width = int(image_dimensions[0] / ratios[1])

    if supposed_image_height < terminal_dimensions[1]:
        return terminal_dimensions[0], supposed_image_height
    # Else
    return supposed_image_width, terminal_dimensions[1]


def get_image_dimensions(img: ImageClass, fontratio: float) -> tuple[int, int]:
    width, height = img.size

    # Compensate for the taller font
    height *= fontratio
    height = int(height)

    return (width, height)


def try_open_image_if_it_exists(path: str) -> ImageClass:
    try:
        return Image.open(path)
    except FileNotFoundError:
        print(f'File not found at "{path}"')
    except UnidentifiedImageError:
        print(f'File at "{path}" is not an image')

    sys.exit(1)

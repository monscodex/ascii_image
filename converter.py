from PIL import Image, UnidentifiedImageError
from os import get_terminal_size
import random
import sys

from PIL.Image import Image as ImageClass

from cli_option_processors import CharacterColoringFunction


def print_ascii_image(
    image_path: str,
    character_coloring_function: CharacterColoringFunction,
    palette: str,
    fontratio: float,
    random_char: bool,
):
    image: ImageClass = try_open_image_if_it_exists(image_path)

    image = resize_image_in_order_to_fit_in_terminal(image, fontratio)

    ascii_representation: str = get_image_ascii_representation(
        image, palette, character_coloring_function, random_char
    )

    print(ascii_representation)


def write_ascii_image(
    image_path: str,
    output_file_path: str,
    character_coloring_function: CharacterColoringFunction,
    palette: str,
    random_char: bool,
    fontratio: float,
    reduction_factor: float,
):
    image: ImageClass = try_open_image_if_it_exists(image_path)

    image = reduce_image_and_compensate_fontratio_pixel_proportion_modification(
        image, fontratio, reduction_factor
    )

    ascii_representation: str = get_image_ascii_representation(
        image, palette, character_coloring_function, random_char
    )

    with open(output_file_path, "w") as f:
        f.write(ascii_representation)


def reduce_image_and_compensate_fontratio_pixel_proportion_modification(
    image: ImageClass, fontratio: float, reduction_factor: float
):
    width, height = get_image_dimensions_respecting_fontratio(image, fontratio)

    reduced_width = width / reduction_factor
    reduced_height = height / reduction_factor

    image = image.resize((int(reduced_width), int(reduced_height)))

    return image


def get_image_ascii_representation(
    image: ImageClass,
    palette: str,
    character_coloring_function: CharacterColoringFunction,
    random_char: bool,
) -> str:
    pixels = image.load()
    width, height = image.size

    text_lines = [
        get_pixel_line_converted_to_text(
            y, width, pixels, palette, character_coloring_function, random_char
        )
        for y in range(height)
    ]

    text_image = "\n".join(text_lines)

    return text_image


def get_pixel_line_converted_to_text(
    y: int,
    width: int,
    pixels,
    palette: str,
    character_coloring_function: CharacterColoringFunction,
    random_char: bool,
) -> str:
    chars = [
        get_pixel_conversion(
            pixels[x, y], palette, character_coloring_function, random_char
        )
        for x in range(width)
    ]

    chars_to_string = "".join(chars)

    return chars_to_string


def get_pixel_conversion(
    pixel: tuple[int, int, int],
    palette: str,
    character_coloring_function: CharacterColoringFunction,
    random_char: bool,
) -> str:
    palette_char = get_corresponding_palette_char(pixel, palette, random_char)

    colored_char = character_coloring_function(palette_char, pixel)

    return colored_char


def get_corresponding_palette_char(
    pixel: tuple[int, int, int], palette: str, random_char: bool
) -> str:
    if random_char:
        return random.choice(palette)

    # The pixel is a tuple with (r, g, b) values
    grey_value = sum(pixel) / 3

    # As the palette is ordered decreasingly, the more gray a pixel is the
    # closer to the start the character will be
    palette_index = (1 - (grey_value / 256)) * len(palette)
    palette_index = int(palette_index)

    palette_index -= 1 if palette_index == len(palette) else 0

    return palette[palette_index]


def resize_image_in_order_to_fit_in_terminal(
    image: ImageClass, fontratio: float
) -> ImageClass:
    # Calculate image's dimensions in order to fit in the terminal without loosing its ratio
    width, height = get_displaying_dimensions(image, fontratio)

    return image.resize((width, height))


def get_displaying_dimensions(image: ImageClass, fontratio: float) -> tuple[int, int]:
    image_dimensions = get_image_dimensions_respecting_fontratio(image, fontratio)
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

    return supposed_image_width, terminal_dimensions[1]


def get_image_dimensions_respecting_fontratio(
    image: ImageClass, fontratio: float
) -> tuple[int, int]:
    width, height = image.size

    # Compensate for the taller font
    height *= fontratio
    height = int(height)

    return (width, height)


def try_open_image_if_it_exists(path: str) -> ImageClass:
    try:
        return Image.open(path)
    except FileNotFoundError:
        print(f'Error: File not found at "{path}"')
    except UnidentifiedImageError:
        print(f'File at "{path}" is not an image')

    sys.exit(1)

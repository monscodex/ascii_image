from PIL import Image, UnidentifiedImageError
from os import get_terminal_size
import random
import sys

def get_ascii_image(path: str, color: str, palette: str, fontratio: float, random_char: bool) -> str:
    img = safely_open_image(path)

    # Calculate image's dimensions in order to fit in the terminal without loosing its ratio
    width, height = get_displaying_dimensions(img, fontratio)
    img = img.resize((width, height))

    ascii_representation = get_ascii_representation(img, palette, color, random_char)

    return ascii_representation

def get_ascii_representation(img: Image, palette_option: str, color: bool, random_char: bool) -> str:
    palette = get_palette_from_option(palette_option)

    pixels = img.load()
    width, height = img.size

    text_image = ""

    for y in range(height):
        # End of line
        text_image += '\n'

        for x in range(width):
            pixel = pixels[x, y]
            pixel_text_conversion = get_pixel_conversion(pixel, palette, color, random_char)

            text_image += pixel_text_conversion

    return text_image

def get_pixel_conversion(pixel: tuple[float, ...], palette : str, color : str, random_char : bool) -> str:
    palette_char = get_corresponding_palette_char(pixel, palette, random_char)

    colored_char = color_char(palette_char, color, pixel)

    return colored_char

def color_char(char : str, color : bool, pixel: tuple[float, ...]) -> str:
    match color:
        case 'full':
            return f"\033[38;2;{pixel[0]};{pixel[1]};{pixel[2]}m{char}"
        case 'b&w':
            # The pixel is a tuple with (r, g, b) values
            grey = int(sum(pixel) / 3)
            return f"\033[38;2;{grey};{grey};{grey}m{char}"
        case 'none':
            return char

def get_palette_from_option(palette_option : str) -> str:
    if palette_option['specified'] != None:
        return palette_option['specified']
    
    match palette_option['code']:
        case 'extended':
            return """ÆÑÊŒØMÉËÈÃÂWQBÅæ#NÁþEÄÀHKRŽœXgÐêqÛŠÕÔA€ßpmãâG¶øðé8ÚÜ$ëdÙýèÓÞÖåÿÒb¥FDñáZPäšÇàhû§ÝkŸ®S9žUTe6µOyxÎ¾f4õ5ôú&aü™2ùçw©Y£0VÍL±3ÏÌóC@nöòs¢u‰½¼‡zJƒ%¤Itocîrjv1lí=ïì<>i7†[¿?×}*{+()/»«•¬|!¡÷¦¯—^ª„”“~³º²–°­¹‹›;:’‘‚’˜ˆ¸…·¨´` """
        case 'standard':
            return """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
        case 'reduced':
            return "@%#*+=-:. "
        case 'block':
            return chr(9608)

def get_corresponding_palette_char(pixel : tuple[float, ...], palette : str, random_char : bool) -> str:
    if random_char:
        return random.choice(palette)
    
    # The pixel is a tuple with (r, g, b) values
    gray_value = sum(pixel) / 3

    # As the palette is ordered decreasingly, the more gray a 
    palette_index =  (1 - (gray_value / 256)) * len(palette)
    palette_index = int(palette_index)

    return palette[palette_index]

def get_displaying_dimensions(img : Image, fontratio : float) -> tuple[int, int]:
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

def get_image_dimensions(img : Image, fontratio : float) -> tuple[int, int]:
    width, height = img.size

    # Compensate for the taller font
    height *= fontratio
    height = int(height)

    return (width, height)

def safely_open_image(path: str) -> Image:
    try:
        return Image.open(path)
    except FileNotFoundError:
        print(f'File not found at "{path}"')
    except UnidentifiedImageError:
        print(f'File at "{path}" is not an image')

    sys.exit(1)
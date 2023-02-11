from typing import Callable
from enum import Enum


class PaletteCode(str, Enum):
    extended = "extended"
    standard = "standard"
    reduced = "reduced"
    block = "block"


class Color(str, Enum):
    full = "full"
    black_and_white = "b&w"
    none = "none"


PALETTES: dict[PaletteCode, str] = {
    PaletteCode.extended: """ÆÑÊŒØMÉËÈÃÂWQBÅæ#NÁþEÄÀHKRŽœXgÐêqÛŠÕÔA€ßpmãâG¶øðé8ÚÜ$ëdÙýèÓÞÖåÿÒb¥FDñáZPäšÇàhû§ÝkŸ®S9žUTe6µOyxÎ¾f4õ5ôú&aü™2ùçw©Y£0VÍL±3ÏÌóC@nöòs¢u‰½¼‡zJƒ%¤Itocîrjv1lí=ïì<>i7†[¿?×}*{+()/»«•¬|!¡÷¦¯—^ª„”“~³º²–°­¹‹›;:’‘‚’˜ˆ¸…·¨´` """,
    PaletteCode.reduced: "@%#*+=-:. ",
    PaletteCode.block: chr(9608),
    PaletteCode.standard: """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`'. """,
}


def get_palette_from_code_if_empty_palette(
    specified_palette: str, palette_code: PaletteCode
) -> str:
    return specified_palette if specified_palette else PALETTES[palette_code]


def get_char_in_pixel_full_color(char: str, pixel: tuple[int, int, int]) -> str:
    return f"\033[38;2;{pixel[0]};{pixel[1]};{pixel[2]}m{char}"


def get_char_in_pixel_black_and_white(char: str, pixel: tuple[int, int, int]) -> str:
    grey_value = int(sum(pixel) / 3)

    return f"\033[38;2;{grey_value};{grey_value};{grey_value}m{char}"


CharacterColoringFunction = Callable[[str, tuple[int, int, int]], str]

CHARACTER_COLORING_FUNCTIONS: dict[Color, CharacterColoringFunction] = {
    Color.full: get_char_in_pixel_full_color,
    Color.black_and_white: get_char_in_pixel_black_and_white,
    Color.none: lambda char, pixel: char,
}

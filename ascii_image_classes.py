from typing import Union
from enum import Enum
from dataclasses import dataclass


class PaletteCode(str, Enum):
    extended = "extended"
    standard = "standard"
    reduced = "reduced"
    block = "block"


@dataclass
class PaletteOption:
    specified: Union[str, None]
    code: PaletteCode


class Color(str, Enum):
    full = "full"
    black_and_white = "b&w"
    none = "none"

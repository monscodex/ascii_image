from PIL import Image
from os import get_terminal_size

# Font ratio between the width over the hight (x/y)
FONT_RATIO = 0.5

def get_ascii_image(path, color, palette_code):
    img = Image.open(path)

    # Calculate image's dimensions in order to fit in the terminal without loosing its ratio
    width, heigth = get_displaying_dimensions(img)
    img = img.resize((width, heigth))

    ascii_representation = get_ascii_representation(img, palette_code, color)

    return ascii_representation

def get_ascii_representation(img, palette_code, color):
    palette = get_palette_from_code(palette_code)

    pixels = img.load()
    width, heigth = img.size

    text_image = ""

    for y in range(heigth):
        for x in range(width):
            pixel = pixels[x, y]
            palette_char = get_corresponding_palette_char(pixel, palette)

            if color:
                text_image += f"\033[38;2;{pixel[0]};{pixel[1]};{pixel[2]}m{palette_char}"
            else:
                text_image += palette_char
        
        # End of line
        text_image += '\n'

    return text_image

def get_palette_from_code(palette_code):
    match palette_code:
        case 'expanded':
            return """ÆÑÊŒØMÉËÈÃÂWQBÅæ#NÁþEÄÀHKRŽœXgÐêqÛŠÕÔA€ßpmãâG¶øðé8ÚÜ$ëdÙýèÓÞÖåÿÒb¥FDñáZPäšÇàhû§ÝkŸ®S9žUTe6µOyxÎ¾f4õ5ôú&aü™2ùçw©Y£0VÍL±3ÏÌóC@nöòs¢u‰½¼‡zJƒ%¤Itocîrjv1lí=ïì<>i7†[¿?×}*{+()/»«•¬|!¡÷¦¯—^ª„”“~³º²–°­¹‹›;:’‘‚’˜ˆ¸…·¨´` """
        case 'reduced':
            return "@%#*+=-:. "
        case 'block':
            return chr(9608)

def get_corresponding_palette_char(pixel, palette):
    # The pixel is a tuple with (r, g, b) values
    gray_value = sum(pixel) / 3

    # As the palette is ordered decreasingly, the more gray a 
    palette_index =  (1 - (gray_value / 256)) * len(palette)
    palette_index = int(palette_index)

    return palette[palette_index]

def get_displaying_dimensions(img):
    image_dimensions = get_image_dimensions(img)
    terminal_dimensions = get_terminal_size()

    ratios = [
        image_d / terminal_d
        for image_d, terminal_d in zip(image_dimensions, terminal_dimensions)
    ]

    # We are calculating the possible adapted image dimensions
    # to then prefer the one that adapts to the terminal's ratio
    supposed_image_heigth = int(image_dimensions[1] / ratios[0])
    supposed_image_width = int(image_dimensions[0] / ratios[1])

    if supposed_image_heigth < terminal_dimensions[1]:
        return terminal_dimensions[0], supposed_image_heigth
    
    # Else
    return supposed_image_width, terminal_dimensions[1]

def get_image_dimensions(img):
    width, heigth = img.size

    # Compensate for the taller font
    heigth *= FONT_RATIO
    heigth = int(heigth)

    return (width, heigth)
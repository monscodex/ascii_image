# Ascii Image Converter

Easily convert your images to ascii with a CLI.

## Examples

### Default settings
```bash
python3 ascii_image.py print-image girl.jpg
```
![Default settings](./output-examples/example.png)

### Extended palette
```bash
python3 ascii_image.py print-image girl.jpg --palette-code extended
```
![Extended palette](./output-examples/example_extended-palette.png)

### Black & White color
```bash
python3 ascii_image.py print-image girl.jpg --color 'b&w'
```
![Black & White](./output-examples/example_black-and-white.png)

### Uncolored + reduced palette
```bash
python3 ascii_image.py print-image girl.jpg --color none --palette-code reduced
```
![Uncolored + reduced palette](./output-examples/example_uncolored_and_reduced-palette.png)
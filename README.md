# Ascii Image Converter

Easily convert your images to ascii with a CLI.

## Examples

```bash
python3 ascii_image.py print-image girl.jpg
```
Terminal output:
![Default settings](./output-examples/example.png)

```bash
python3 ascii_image.py print-image girl.jpg --palette-code extended
```
Terminal output:
![Extended palette](./output-examples/example_extended-palette.png)

```bash
python3 ascii_image.py print-image girl.jpg --color 'b&w'
```
Terminal output:
![Black & White](./output-examples/example_black-and-white.png)

```bash
python3 ascii_image.py print-image girl.jpg --color none --palette-code reduced
```
Terminal output:
![Uncolored + reduced palette](./output-examples/example_uncolored_and_reduced-palette.png)
import os
import json
from PIL import Image

im = Image.open('unknown.png')
colors = {}

def split_into_rows(im, row_height, col_width):
    y = 0
    while y < row_height:
        x = 0
        print(y, x,)
        print( x < col_width)
        while x < col_width:
            print(f'x: {x}, y: {y}')
            top_left = ((x/col_width)*im.width, (y/row_height)*im.height)
            bottom_right = (min((x/col_width)*im.width + 1/col_width*im.width, im.width), min((y/row_height)*im.height + 1/row_height*im.height, im.height))
            image = im.crop((*top_left, *bottom_right))
            save_path = os.path.join(OUTPUT_DIR, f'{x}{y}.png')

            image.save(save_path)
            color = image.getpixel((image.width/2, image.height/2))
            hex = "{0:02x}{1:02x}{2:02x}".format(color[0], color[1], color[2])
            colors[f'{x+74},{y+117}'] = hex
            yield image

            x += 1

        y += 1

OUTPUT_DIR = 'output'

for i, row in enumerate(split_into_rows(im, 30, 52)):
    save_path = os.path.join(OUTPUT_DIR, f'{i}.png')

    row.save(save_path)

# dump colors as json to file
with open('colors.json', 'w') as f:
    json.dump(colors, f)

# array of all coords in colors that have hex e50000
red_pixels = []
for coord, hex in colors.items():
    if hex == 'e50000':
        red_pixels.append(coord)

with open('red.json', 'w') as f:
    json.dump(red_pixels, f)

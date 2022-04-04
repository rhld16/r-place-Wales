import os
import json
from PIL import Image

im = Image.open('unknown.png')
colors = {}

def get_dominant_color(pil_img, palette_size=16):
    # Resize image to speed up processing
    img = pil_img.copy()
    img.thumbnail((100, 100))

    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]

    return dominant_color

def split_into_rows(im, row_height, col_width):
    y = 0
    while y < row_height:
        x = 0
        while x < col_width:
            top_left = ((x/col_width)*im.width, (y/row_height)*im.height)
            bottom_right = (min((x/col_width)*im.width + 1/col_width*im.width, im.width), min((y/row_height)*im.height + 1/row_height*im.height, im.height))
            image = im.crop((*top_left, *bottom_right))
            save_path = os.path.join(OUTPUT_DIR, f'{x+67},{y+115}.png')

            image.save(save_path)
            color = get_dominant_color(image)
            if (x < 81-67 and y < 137-115):
                x += 1
                continue
            hex = "{0:02x}{1:02x}{2:02x}".format(color[0], color[1], color[2])
            colors[f'{x+67},{y+115}'] = hex
            yield image

            x += 1

        y += 1

OUTPUT_DIR = 'output'

for i, row in enumerate(split_into_rows(im, 32+1, 63+1)):
    save_path = os.path.join(OUTPUT_DIR, f'{i}.png')

with open('colors.json', 'w') as f:
    json.dump(colors, f)

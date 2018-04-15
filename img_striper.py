#! /usr/bin/env python3

import argparse
import textwrap
import math
from PIL import Image

parser = argparse.ArgumentParser(
    prog='img_striper.py',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
        Image striper

        This is a simple program to make stripes out of images
        and join them together again. It was inspired by this great
        video: https://www.instagram.com/p/BhZU4XMgdYA/

        This script follows the WTFPL, so go ahead and do whatever
        the fuck you want with it.
    '''),
    epilog=textwrap.dedent('''\
        This is just a simple exercise.
        Please don't hate me for my noobiness.
    '''))

parser.add_argument('--i',
                    '-input',
                    help='File to be shifted',
                    type=argparse.FileType('rb', 0),
                    required=True
                    )

parser.add_argument('--o',
                    '-output',
                    help='Image to be saved',
                    type=argparse.FileType('wb', 0),
                    required=True
                    )

args = parser.parse_args()

# open image and create new one
original_doggo = Image.open(args.i)
original_w, original_h = original_doggo.size
inter_w = int(math.floor(original_w / 2))
inter_h = original_h * 2
inter_doggo = Image.new('RGB', [inter_w, inter_h], 'white')

# calculate the number of strips
no_strips = int(math.floor(original_w / 15))

for n in range(0, no_strips):
    # calculate xs from the cropped strip
    x1 = n * 15
    x2 = x1 + 15
    # create crop box
    crop_box = (x1, 0, x2, original_h)
    # cropped section
    section = original_doggo.crop(crop_box)

    y1 = 0

    # calculate xs for the placement of the paste
    if n % 2:
        y1 = original_h

    y2 = y1 + original_h
    x3 = 15 * int(math.floor(n / 2))
    x4 = x3 + 15
    paste_box = (x3, y1, x4, y2)

    inter_doggo.paste(section, paste_box)

original_w, original_h = inter_doggo.size
new_h = int(math.floor(inter_h / 2))
new_w = inter_w * 2
new_doggo = Image.new('RGB', [new_w, new_h], 'white')

# calculate the number of strips
no_strips = int(math.floor(inter_h / 15))

for n in range(0, no_strips):
    # calculate xs from the cropped strip
    y1 = n * 15
    y2 = y1 + 15
    # create crop box
    crop_box = (0, y1, inter_w, y2)
    # cropped section
    section = inter_doggo.crop(crop_box)

    x1 = 0

    # calculate xs for the placement of the paste
    if n % 2:
        x1 = inter_w

    x2 = x1 + inter_w
    y3 = 15 * int(math.floor(n / 2))
    y4 = y3 + 15
    paste_box = (x1, y3, x2, y4)

    new_doggo.paste(section, paste_box)

new_doggo.save(args.o)

# print(original_w, original_h)
# parser.print_help()

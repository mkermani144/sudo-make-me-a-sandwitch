'''
This script generates a color pallete containing the colors which are most used
in a picture.
'''
import sys
from PIL import Image
from collections import Counter as counter
from optparse import OptionParser


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

parser = OptionParser('Usage: color-palette [options] <image>')
parser.add_option(
    '-l', '--palette-length',
    dest='palette_length',
    default=5,
    type='int',
    help='set number of colors in the palette')
parser.add_option(
    '-t', '--treshold',
    dest='treshold',
    default=50,
    type='int',
    help='set treshold of difference between colors')
parser.add_option(
    '-s', '--scale-down',
    dest='scaledown',
    default=1,
    type='int',
    help='set how much the image should be scaled down')

options, args = parser.parse_args()
treshold = options.treshold
palette_length = options.palette_length
scaledown = options.scaledown
if len(args) == 0:
    parser.error('No image specified.')

image = Image.open(args[-1])
try:
    ratio = 1/scaledown
except Exception as e:
    print(e)
    exit(1)
image.thumbnail((image.size[0]*ratio, image.size[1]*ratio), Image.ANTIALIAS)
image_pixels = image.getdata()
image_pixels = [(x[0], x[1], x[2]) for x in image_pixels]
image_dict = dict(counter(image_pixels))
image_twins = [(image_dict[i], i) for i in image_dict]
image_twins.sort(reverse=True)
temp = []
current = 0
while palette_length:
    m = image_twins[current][1]
    image_dict.pop(m)
    isSimilar = False
    for el in temp:
        if sum(abs(x - y) for (x, y) in zip(m, el)) < treshold:
            isSimilar = True
    if len(temp) and not isSimilar:
        print('\x1b[38;2;{};{};{}m{}{} {}\x1b[0m'.format(
            m[0], m[1], m[2],
            '\u2588', '\u2588',
            rgb_to_hex(m)))
        palette_length -= 1
        temp.append(m)
    elif len(temp) == 0:
        print('\x1b[38;2;{};{};{}m{}{} {}\x1b[0m'.format(
            m[0], m[1], m[2],
            '\u2588', '\u2588',
            rgb_to_hex(m)))
        palette_length -= 1
        temp.append(m)
    current += 1

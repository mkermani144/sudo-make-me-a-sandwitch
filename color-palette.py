'''
This script generates a color pallete containing the colors which are most used
in a picture.
'''
import sys
from PIL import Image
from collections import Counter as counter

if not 1 < len(sys.argv) < 5:
    print('Usage: color-palette <image> [<palette-length>] [<treshold>]')
    exit(1)
try:
    treshold = int(sys.argv[3])
except:
    treshold = 50
try:
    palette_length = int(sys.argv[2])
except:
    palette_length = 5
image = Image.open(sys.argv[1])
image_pixels = image.getdata()
image_pixels = [(x[0], x[1], x[2]) for x in image_pixels]
image_dict = dict(counter(image_pixels))
temp = []
while palette_length:
    m = max(image_dict, key=image_dict.get)
    image_dict.pop(m)
    isSimilar = False
    for el in temp:
        if abs(m[0] - el[0]) + abs(m[1] - el[1]) + abs(m[2] - el[2]) < treshold:
            isSimilar = True
    if len(temp) and not isSimilar:
        print('\x1b[38;2;{};{};{}m{}{} rgb({}, {}, {})\x1b[0m'.format(m[0], m[1], m[2], '\u2588', '\u2588', m[0], m[1], m[2]))
        palette_length -= 1
        temp.append(m)
    elif len(temp) == 0:
        print('\x1b[38;2;{};{};{}m{}{} rgb({}, {}, {})\x1b[0m'.format(m[0], m[1], m[2], '\u2588', '\u2588', m[0], m[1], m[2]))
        palette_length -= 1
        temp.append(m)

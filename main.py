from typing import Tuple
import cv2
import numpy as np
import os
import math

# Contrast ( source, constast_multiplier, source, 0, brightness )
# source = cv2.addWeighted(source, 2, source, 0, -127)

mean_brightness = 150


def rgb_to_hsv(r, g, b):
    _r = r / 255
    _g = g / 255
    _b = b / 255

    cmax = max([_r, _g, _b])
    cmin = min([_r, _g, _b])
    delta = cmax - cmin

    hue = None

    if delta == 0:
        hue = 0
    elif cmax == _r:
        hue = 60 * (((_g - _b) / delta) % 6)
    elif cmax == _g:
        hue = 60 * (((_b - _r) / delta) + 2)
    else:
        hue = 60 * (((_r - _g) / delta) + 4)

    saturation = None

    if cmax == 0:
        saturation = 0
    else:
        saturation = delta / cmax

    value = cmax

    return tuple([round(hue, 1), round(saturation * 100, 1), round(value * 100, 1)])


def find_matching_pixel(img, min_color, max_color):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, min_color, max_color)
    return dict(zip(('x', 'y'), np.unravel_index(np.argmax(mask), mask.shape)[::-1]))


def is_nearby_dotes(coords1, coords2, radius=20):
    return abs(coords1[0] - coords2[0]) <= radius and abs(coords1[1] - coords2[1]) <= radius


def change_brightness(img, value):
    if not (-100 <= value <= 100):
        raise ValueError('Value must be between -100 and 100')
    print('Brightness at:', value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    if value > 0:
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
    else:
        value *= -1
        v[v < value] = 0
        v[v >= value] -= value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def correct_brightness(img):
    mean = np.mean(img)
    if mean == mean_brightness:
        return img
    if mean > mean_brightness:
        img = change_brightness(img, -int(mean - mean_brightness))
    else:
        img = change_brightness(img, int(mean_brightness - mean))

    return img

# TODO
def clear_near_dots(collection, key, radius=50):
    pass

# TODO
def adaptive_search(img, find_level):
    pass


path = './bears/withBears/'

for i in os.listdir(path):
    source = cv2.imread(path + i)
    source = cv2.resize(source, (1800, 1000))
    source = correct_brightness(source)
    source = cv2.addWeighted(source, 2, source, 0, -127)

    # source = cv2.addWeighted(source, 2, source, 0, -127)

    # HUE - 40..50

    mean = []

    for row in range(len(source)):
        for cell in range(len(source[row])):
            _cell = list(source[row][cell])
            hsv = rgb_to_hsv(*_cell[::-1])
            # Compare hue
            if 45 <= hsv[0] <= 60:
                # Compare saturation
                if 10 <= hsv[1]:
                    # Compare value
                    if 20 <= hsv[2]:
                        mean.append(((cell, row), hsv))

    # mean = clear_near_dots(mean, key=lambda x: x[0])
    # print(*mean, sep='\n')

    # SHOWING IMAGE
    cv2.imshow('img', source)
    cv2.waitKey(0)

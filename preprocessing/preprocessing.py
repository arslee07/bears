import typing
from utils import Utils
import cv2
import numpy as np
import math

# Contrast ( source, constast_multiplier, source, 0, brightness )
# source = cv2.addWeighted(source, 2, source, 0, -127)


class Preprocessor:
    # Сет файла для работы с оным
    def __init__(self, file: str or np.ndarray) -> None:
        if type(file) is str:
            self.file = cv2.imread(file)
        elif type(file) is np.ndarray:
            self.file = file
        else:
            print(type(file))
            raise ValueError('Invalid file type!')
        Preprocessor.compressor = 1

    # Получить точки с оранжевым оттенком
    def get_dots(self, compress_multimplier: int = 4):
        self.compressor = compress_multimplier
        file = self.file
        img = Utils.default_image_preprocessing(cv2.resize(
            file,
            (math.floor(file.shape[1] / compress_multimplier),
             math.floor(file.shape[0] / compress_multimplier))
        ))
        def hsv_check(h, s, v):
            return 30 < h < 60 and \
                   15 < s and \
                   40 < v
        dots = []
        for row in range(len(img)):
            for cell in range(len(img[row])):
                hsv = Utils.rgb_to_hsv(*list(img[row][cell])[::-1])
                if hsv_check(*hsv):
                    dots.append([cell, row])

        return Utils.clear_nearby_dots(dots)

    # Показать текузий файл
    def show(self):
        cv2.imshow('Image', self.file)
        cv2.waitKey(0)

    # Вырезать квадраты с точками
    def get_rects(self, dots, side=100):
        size = math.floor(side / 2)
        rects = []
        img = self.file
        height, width = img.shape[:2]
        for (index, item) in enumerate(dots):
            dot = [item[0] * self.compressor, item[1] * self.compressor]
            
            # TOP BOTTOM LEFT RIGHT
            sides = {
                'top': dot[1] - size,
                'bottom': dot[1] + size,
                'left': dot[0] - size,
                'right': dot[0] + size
            }

            if sides['top'] < 0:
                sides['bottom'] += abs(sides['top'])
                sides['top'] = 0
            
            if sides['bottom'] > height:
                sides['top'] -= sides['bottom'] - height
                sides['bottom'] = height - 1
            
            if sides['left'] < 0:
                sides['right'] += abs(sides['left'])
                sides['left'] = 0
            
            if sides['right'] > width:
                sides['left'] -= sides['right'] - width
                sides['right'] = width - 1
            
            rects.append(img[sides['top']:sides['bottom'], sides['left']:sides['right']])
        return rects
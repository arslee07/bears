from typing import Any, List, Tuple, Callable
from utils import Utils
import cv2
import numpy as np
import os
import math

# Contrast ( source, constast_multiplier, source, 0, brightness )
# source = cv2.addWeighted(source, 2, source, 0, -127)


class Preprocessor:
    # Сет файла для работы с оным
    @staticmethod
    def set_file(file_path: str) -> None:
        Preprocessor.file = cv2.imread(file_path)
        Preprocessor.compressor = 1

    # Получить точки с оранжевым оттенком
    @staticmethod
    def get_dots(compress_multimplier: int = 4):
        Preprocessor.compressor = compress_multimplier
        file = Preprocessor.file
        img = Utils.default_image_preprocessing(cv2.resize(
            file,
            (math.floor(file.shape[1] / compress_multimplier),
             math.floor(file.shape[0] / compress_multimplier))
        ))
        def hue(x): return 30 < x < 60
        dots = []
        for row in range(len(img)):
            for cell in range(len(img[row])):
                hsv = Utils.rgb_to_hsv(*list(img[row][cell])[::-1])
                if hue(hsv[0]):
                    dots.append([cell, row])

        return Utils.clear_nearby_dots(dots)

    # Показать текузий файл
    @staticmethod
    def show():
        cv2.imshow('Image', Preprocessor.file)
        cv2.waitKey(0)

    # Вырезать квадраты с точками
    @staticmethod
    def get_rects(dots, side=100):
        size = math.floor(side / 2)
        rects = []
        img = Preprocessor.file
        height, width = img.shape[:2]
        for (index, item) in enumerate(dots):
            dot = [item[0] * Preprocessor.compressor, item[1] * Preprocessor.compressor]
            
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
            
            if sides['right'] > height:
                sides['left'] -= sides['right'] - height
                sides['right'] = width - 1
            
            rects.append(img[sides['top']:sides['bottom'], sides['left']:sides['right']])
        return rects
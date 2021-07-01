from typing import List, Tuple
import numpy as np
import cv2


class Utils:
    # Значение для нормализации яркости изображений
    mean_brightness = 150

    # Функция конвертации из RBG в HSV
    @staticmethod
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

        return tuple([
            round(hue, 1),
            round(saturation * 100, 1),
            round(value * 100, 1)
        ])

    # Возвращает True если расстояние между X координатой точек меньше переменно
    # Тоже самое с Y координатой
    @staticmethod
    def is_nearby_dots(coords1: Tuple[int, int], coords2: Tuple[int, int], radius: int = 20):
        return abs(coords1[0] - coords2[0]) <= radius and \
               abs(coords1[1] - coords2[1]) <= radius

    # Удаляет все точки находящиеся в близости с другими в опр радиусе
    @staticmethod
    def clear_nearby_dots(dots: List[List[int]], rng=200) -> List[Tuple[int, int]]:
        dots.sort(key=lambda x: x[0])
        current = dots[0]
        result = [current]
        for dot in dots:
            if not Utils.is_nearby_dots(current, dot, rng):
                result.append(dot)
                current = dot
        return result

    # Меняет яркость всего изображения на определенное значение
    @staticmethod
    def change_brightness(img, value):
        if not (-100 <= value <= 100):
            raise ValueError('Value must be between -100 and 100')
        # print('Brightness at:', value)
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

    # Корректирует средннюю яркость до константы выше ( mean_brightness )
    @staticmethod
    def correct_brightness(img):
        mean = np.mean(img)
        if mean == Utils.mean_brightness:
            return img
        if mean > Utils.mean_brightness:
            img = Utils.change_brightness(
                img, -int(mean - Utils.mean_brightness))
        else:
            img = Utils.change_brightness(
                img, int(Utils.mean_brightness - mean))

        return img

    # Просто чтобы не писать каждый раз xD
    @staticmethod
    def default_image_preprocessing(img):
        img = Utils.correct_brightness(img)
        return cv2.addWeighted(img, 2, img, 0, -127)

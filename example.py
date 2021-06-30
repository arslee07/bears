from utils import Utils
from preprocessing import Preprocessor
from cv2 import imshow, waitKey

path = 'some path'
Preprocessor.set_file(path)

dots = Preprocessor.get_dots()
print(*dots, sep='\n')
rects = Preprocessor.get_rects(dots, 200)

imshow('img', rects[0])
waitKey(0)
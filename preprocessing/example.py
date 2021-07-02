from utils import Utils
from preprocessing import Preprocessor
from cv2 import imshow, waitKey

path = 'bears_data/withBears/_2016-04-25 11-06-03_2568_L.JPG'
Preprocessor = Preprocessor(path)

dots = Preprocessor.get_dots()
print(*dots, sep='\n')
rects = Preprocessor.get_rects(dots, 200)

for i in rects:
    imshow('img', i)
    waitKey(0)
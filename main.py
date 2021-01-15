import cv2

from utils import *
from Yolo import YOLO


image = cv2.imread('images/test.jpg')

detector = YOLO()
cv2.imshow('img', detector.detect_photo(image))
cv2.waitKey(0)
cv2.destroyAllWindows()
import threading
import traceback
from car_centroid_tracker import program
from car_centroid_tracker import utils
from client import OnlineClassificatorClient
import cv2
import time

googleColabClient = OnlineClassificatorClient('http://806f115955e1.ngrok.io')

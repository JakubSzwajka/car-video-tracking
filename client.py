
from __future__ import print_function
import requests
import json
import cv2
VIDEO_PATH = 'videos/droga.mp4'
# SERVER_IP = '192.168.0.17:5000/detect'
SERVER_IP = 'http://localhost:5000/detect'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('images/test.jpg')
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(SERVER_IP, data=img_encoded.tobytes(), headers=headers)
# decode response
print(json.loads(response.text))
# print()

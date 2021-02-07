
import requests
import json
import cv2

# use it like:
# googleColabClient = OnlineClassificatorClient('http://806f115955e1.ngrok.io')


class OnlineClassificatorClient():

    def __init__(self,endpoint):
        self.endpoint = endpoint
        self.content_type = 'image/jpeg'
        self.headers = {'content-type': self.content_type}
        
    def detection(self, image):
        method = '/detect'
        _, img_encoded = cv2.imencode('.jpg', image)
        response = requests.post(self.endpoint + method, data=img_encoded.tobytes(), headers=self.headers)
        return json.loads(response.text)
        


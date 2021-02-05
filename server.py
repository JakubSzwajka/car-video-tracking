from flask import Flask, request, Response
from yolo.Yolo import YOLO
import cv2
import numpy as np 
import jsonpickle

# init Flask application
app = Flask(__name__)

@app.route("/detect", methods=['POST'])
def get_detections():
    req = request
    nparr = np.frombuffer(req.data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # imageProcessed = detector.detect_photo(image)
    # cv2.imshow('image', imageProcessed )
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # build a response dict to send back to client
    response = {
        'message': 'image received. size={}x{}'.format(image.shape[1], image.shape[0] )
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == "__main__": 
    # init detector 
    detector = YOLO()
    
    # turn on server 
    app.run(host='0.0.0.0', debug=True)

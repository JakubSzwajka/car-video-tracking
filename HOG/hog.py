
import numpy as np
import cv2
import time 
import imutils
from imutils.object_detection import non_max_suppression

class HOGdetector(object):

    LOGGER = False

    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        

    def detect_photo(self, image):
        t1 = time.time()

        image = imutils.resize(image, width=min(400, image.shape[1]))
        orig = image.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        (rects, weights) = self.hog.detectMultiScale(image, winStride=(4, 4),
            padding=(8, 8), scale=1.05)

        for (x, y, w, h) in rects:
            # cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # apply non-maxima suppression to the bounding boxes using a
            # fairly large overlap threshold to try to maintain overlapping
            # boxes that are still people
            rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
            pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
            # draw the final bounding boxes
            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        print(time.time() - t1 )
        return image

detector = HOGdetector( )

capture = cv2.VideoCapture('../videos\sklep_yt.mp4')
# capture = cv2.VideoCapture(0)
while True: 
    ret , frame = capture.read()
    frame = detector.detect_photo(frame)
    cv2.imshow('image', detector.detect_photo(frame))
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
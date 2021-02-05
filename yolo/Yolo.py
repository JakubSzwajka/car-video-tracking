import numpy as np
import cv2
import time
from .utils import * 

class YOLO(object):
    COCONAMES_PATH = "yolo/yolo-coco/coco.names"
    WEIGHTS_PATH = "yolo/yolo-coco/yolov3-spp.weights"
    CONFIG_PATH = "yolo/yolo-coco/yolov3-spp.cfg"

    CONFIDENCE = 0.5
    THRESHOLD = 0.3

    LOGGER = False

    
    def __init__(self):
        # load the COCO class labels    
        self.LABELS = open(self.COCONAMES_PATH).read().strip().split("\n")
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),dtype="uint8")

        # load our YOLO object detector trained on COCO dataset (80 classes)
        logger("loading YOLO from disk..." ,self.LOGGER)
        self.net = cv2.dnn.readNetFromDarknet(self.CONFIG_PATH, self.WEIGHTS_PATH)
        logger("YOLO loaded" ,self.LOGGER) 

        # determine only the *output* layer names that we need from YOLO
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect_photo(self, img): 
        
        # initialize our lists of detected bounding boxes, confidences,
        # and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        start_time = time.time()
        
        (H, W) = img.shape[:2]
        # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416),
            swapRB=True, crop=False)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.ln)
        
        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.CONFIDENCE:
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.CONFIDENCE,
            self.THRESHOLD)
        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                # draw a bounding box rectangle and label on the frame
                color = [int(c) for c in self.COLORS[classIDs[i]]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.LABELS[classIDs[i]],
                    confidences[i])
                cv2.putText(img, text, (x, y - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        else:
            logger(f"No bounding boxes with confidence:{self.CONFIDENCE} and over threshold:{self.THRESHOLD}")
        
        logger(f"Image detection completed in:{time.time() - start_time}")
        return img
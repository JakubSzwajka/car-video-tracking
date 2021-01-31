from typing import OrderedDict
import cv2
import math
import settings
from Tracking_exception import *


class Tracker:
    objets = []
    objectsToClassify = []
    lostObjects = []

    def registerNewObjects(valid_contours, current_frame):
        for contour in valid_contours: 
            if Tracker.isNewObject(contour):
                objectPicture = Tracker.getObjectPicture(contour, current_frame)
                cv2.imshow("car", objectPicture)
                Tracker.registerObject(contour, objectPicture)

    def registerObject(contour, objectPicture):
        x,y,w,h = contour
        newObject = FrameObject(x,y, id=len(Tracker.objets) + 1 , w = w, h = h, objImg = objectPicture)
        Tracker.objets.append(newObject)
        Tracker.objectsToClassify.append(newObject)
        
    def getObjectPicture(contour, current_frame):
        x,y,w,h = contour
        return current_frame.frame[y:y+h, x:x+w]

    def isNewObject(contour):
        x,y,w,h = contour
        to_append = True
        tmp_car = FrameObject(x,y, id='tmp_dummy')
        
        for index, car in enumerate(Tracker.objets):
            if tmp_car == car:
                to_append = False
                Tracker.objets[index].update(x,y,w,h)
                break
        return to_append
    

class FrameObject():
    def __init__(self, x, y, id = 0, w = 1, h = 1, maxDisappeared=10, objImg = None):
        self.ID = id
        self.label = "Not defined"
        self.maxDisappeared = maxDisappeared
        self.disappearedLeft = maxDisappeared
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.updated = False
        self.disappeared = False
        self.objImg = objImg

    def __str__(self):
        return self.ID

    def __eq__(self, other: object):
        if math.dist( [self.x, self.y], [other.x , other.y]) < 150 and self.disappeared == False:
            return True
        else: 
            return False
        
    def update(self, x, y, w, h):
        self.x = x 
        self.y = y 
        self.width = w 
        self.height = h
        self.updated = True
        self.disappearedLeft = self.maxDisappeared 

    def printOnFrame(self, frame):
        if self.updated == False:
            self.disappearedLeft -= 1

            if self.disappearedLeft == 0:
                self.disappeared = True
                raise Tracking_Exception("car disaapear")

        if self.disappeared == False: 
            cv2.rectangle(frame, (self.x, self.y),(self.x + self.width, self.y + self.height), settings.GREEN, 2)
            # label = "CAR ID:" + str(self.ID) + " x: " + str(self.x) + " y: " + str(self.y) 
            label = self.label
            cv2.putText(frame, label, (self.x, self.y), cv2.FONT_HERSHEY_SIMPLEX , 0.8, settings.GREEN, 1, cv2.LINE_AA)
            self.updated = False

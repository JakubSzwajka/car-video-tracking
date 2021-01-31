import cv2
import numpy as np
from Tracking_exception import Tracking_Exception 

class Frame:
    frame_width = 0
    frame_heigh = 0
    
    def __init__(self, frame):
        self.frame = frame
        self.threshold = 100

    def getGreyScale(self):
        return cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

    def getBinary(self, threshold = 100 ):
        return Frame(cv2.threshold( self.frame, threshold, 255, cv2.THRESH_BINARY )[1])
    
    def getDifferenceFrame(self, frame_obj: "Frame"): 
        return Frame(cv2.absdiff(self.getGreyScale(), frame_obj.getGreyScale()))

    def getDilated(self, iterations = 10):
        kernel = np.ones((3,3), np.uint8)
        return Frame(cv2.dilate(self.frame, kernel, iterations=iterations))

    def getFrame(self):
        return self.frame

    def findObjects(self, minContourZone):
        valid_contours = []
        for cntr in self.findContours(): 
            if cv2.contourArea(cntr) >= minContourZone:
                valid_contours.append(cv2.boundingRect(cntr))
        return valid_contours


    def findContours(self):
        return cv2.findContours(self.frame.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)[0]

    def addLine(self, start_point, end_point, color = (124,252,0), thicknes = 10):
        cv2.line(self.frame, start_point, end_point,color, thicknes)

    def putText(self, text, position, font = cv2.FONT_HERSHEY_SIMPLEX, color = (124,252,0), size = 1 , thicknes = 2): 
        cv2.putText(self.frame, text, position, font , size , color, thicknes, cv2.LINE_AA)
    
    def show(self):
        cv2.imshow('frame', self.frame)

    def addBoundingBoxesFromContours(self, Tracker):
        for car in Tracker.objets:
            try: 
                car.printOnFrame( self.frame )
            except Tracking_Exception as error:
                Tracker.lostObjects.append(car) 
                Tracker.objets.remove(car)
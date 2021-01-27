import numpy as np
import cv2
import time
from numpy.core.numeric import count_nonzero 
import copy 

import settings 
import Tracker
import utils
from Frame import Frame
from Tracking_exception import *
from Tracker import Tracker
from utils import FPS


def main( cap ):
    Frame.frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    Frame.frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    first_go = True
    frame = None
    current_frame = None
    previous_frame = None

    while(True):
        if first_go != True:
            previous_frame = Frame(current_frame.getFrame())
        
        ret, frame = cap.read()
        if ret == False: 
            break
        else:
            current_frame = Frame(frame)
        
        if first_go != True:

            # Get difference between current and previous  
            difference_frame = current_frame.getDifferenceFrame(previous_frame)
            
            # Get binary 
            thresholded_frame = difference_frame.getBinary(threshold = 100)
            
            # image dilation
            dilated_frame = thresholded_frame.getDilated( iterations = 10)
            
            # find contours
            valid_contours = dilated_frame.findObjects( minContourZone = settings.MIN_COUNTOUR_ZONE )
            Tracker.filter(valid_contours)

            # set which frame to display for user
            ready_frame = current_frame            
            
            ready_frame.addBoundingBoxesFromContours(Tracker)
            
            ready_frame.putText( FPS.tick(), (7, 70)) 
            ready_frame.putText(str(Tracker.cars_passed), (int(Frame.frame_width) - 100, 70) )

            # start_point = (0, int( Frame.frame_height * settings.DETECTION_ZONE))
            # end_point = ( int(Frame.frame_width) ,int( Frame.frame_height * settings.DETECTION_ZONE)) 
            # ready_frame.addLine(start_point,end_point)
            
            ready_frame.show()
        else: 
            # Display first frame
            first_go = False
            current_frame.show()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            utils.logger('cars found: ' + str(len(Tracker.car_list)), settings.LOG)
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture = utils.read_video('../videos/droga.mp4')
    main(capture)
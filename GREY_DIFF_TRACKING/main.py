import numpy as np
import cv2
import time
from numpy.core.numeric import count_nonzero 

import settings 
import Tracker
from Tracking_exception import *
from Tracker import Car

def logger( message, log = False):
    if log: print(f'{time.ctime()}', message)


def read_video( path ):
    cap = cv2.VideoCapture(path)
    if cap.isOpened():
        logger('Video: ' + path + ' opened')
    else:
        raise Tracking_Exception('File not found')
    return cap

def add_fps(frame, counter, last_frame_time, fps):
    counter += 1
    if time.time() - last_frame_time > 1:
        last_frame_time = time.time()
        fps = counter
        counter = 0
    cv2.putText(frame, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX , 2, settings.GREEN, 3, cv2.LINE_AA) 
    return last_frame_time
   
def main( cap ):

    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    first_go = True
    previous_frame = None
    frame = None
    FPS_counter = 0
    FPS = 0
    FPS_timer = 0 
    car_list = []
    cars_passed = 0

    while(True):
        # time.sleep(0.1)
        
        # Capture frame-by-frame
        if first_go != True:
            previous_frame = frame
        ret, frame = cap.read()
        
        if ret == False: 
            break
        # change frame ---------------------

        # # Our operations on the frame come here
        if first_go != True:
            # Two frames as grayscale
            grayB = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY )
            grayA = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Get difference between previous two 
            difference_frame = cv2.absdiff(grayA, grayB)
            # Get binary 
            ret, thresholded_frame = cv2.threshold(difference_frame, 100, 255, cv2.THRESH_BINARY)
            # image dilation
            kernel = np.ones((3,3), np.uint8)
            dilated = cv2.dilate(thresholded_frame, kernel, iterations = 10)

            # set which frame to display for user
            ready_frame  = frame

            # CONTOURS PART
            # find contours
            contours, _ = cv2.findContours(dilated.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            valid_contours = []

            # filter contours and register them
            for i, cntr in enumerate(contours): 
                x,y,w,h = cv2.boundingRect(cntr)

                if y >= frame_height * settings.DETECTION_ZONE and cv2.contourArea(cntr) >= settings.MIN_COUNTOUR_ZONE:
                    valid_contours.append(cntr)
                    x,y,w,h = cv2.boundingRect(cntr)
                    
                    Tracker.register_car(x,y,w,h,car_list)

            # Print registered cars on frame
            for car in car_list:
                try:
                    car.print_on_frame(ready_frame)
                except Tracking_Exception as error:
                    car_list.remove(car)
                    cars_passed += 1 


            #  ----------------------------------
            #   FPS
            FPS_counter += 1
            if time.time() - FPS_timer > 1:
                FPS_timer = time.time()
                FPS = FPS_counter
                FPS_counter = 0
            cv2.putText(ready_frame, str(FPS), (7, 70), cv2.FONT_HERSHEY_SIMPLEX , 2, settings.GREEN, 3, cv2.LINE_AA) 

            # cars passed  
            cv2.putText(ready_frame, str(cars_passed), (int(frame_width) - 100, 70), cv2.FONT_HERSHEY_SIMPLEX , 2, settings.GREEN, 3, cv2.LINE_AA) 
            # add some lines to image
            start_point = (0, int( frame_height * settings.DETECTION_ZONE))
            end_point = ( int(frame_width) ,int( frame_height * settings.DETECTION_ZONE)) 
            cv2.line(ready_frame, start_point, end_point,(124,252,0), 10)
    
            # Display the resulting frame
            cv2.imshow('frame',ready_frame)
        else: 
            # Display first frame
            first_go = False
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger('cars found: ' + str(len(car_list)), settings.LOG)
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture = read_video('../videos/droga.mp4')
    main(capture)
import numpy as np
import cv2
import time

from numpy.core.numeric import count_nonzero 

from Tracking_exception import *
from Tracker import Car

cap = cv2.VideoCapture('../videos/droga.mp4')
FRAME_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
FRAME_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
DETECTION_ZONE = 0.2
MIN_COUNTOUR_ZONE = 25000
LOG = True
GREEN = (127,200,0)


first_go = True
previous_frame = None
frame = None

FPS_counter = 0
FPS = 0
FPS_timer = 0 

car_list = []

def logger( message, log = False):
    if log: print(f'{time.ctime()}', message)

def register_car(x,y,w,h):
    to_append = True
    tmp_car = Car(x,y, id='tmp')
    for index, car in enumerate(car_list):
        if tmp_car == car:
            to_append = False
            #update here 
            car_list[index].update(x,y,w,h)
            break

    if to_append:
        car_list.append(Car(x,y, id=len(car_list ) + 1 , w = w, h = h))


if cap.isOpened():
    logger('Video opened')
else:
    logger('file not found')

while(True):
    # time.sleep(1)
    
    # Capture frame-by-frame
    if first_go != True:
        previous_frame = frame
    ret, frame = cap.read()
    
    if ret == False: 
        break
    # change frame ---------------------

    # # Our operations on the frame come here
    if first_go != True:
        grayB = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY )
        grayA = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # binary
        difference_frame = cv2.absdiff(grayA, grayB)
        ret, thresholded_frame = cv2.threshold(difference_frame, 100, 255, cv2.THRESH_BINARY)
    
        # image dilation
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(thresholded_frame, kernel, iterations = 10)

        # set which frame to display 
        ready_frame  = frame

        # contours part
        contours, hierarchy = cv2.findContours(dilated.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        valid_contours = []
        for i, cntr in enumerate(contours): 
            x,y,w,h = cv2.boundingRect(cntr)

            if y >= FRAME_HEIGHT * DETECTION_ZONE and cv2.contourArea(cntr) >= MIN_COUNTOUR_ZONE:
                valid_contours.append(cntr)
                x,y,w,h = cv2.boundingRect(cntr)
                register_car(x,y,w,h)


        for car in car_list:
            try:
                car.print_on_frame(ready_frame)
            except Tracking_Exception as error:
                car_list.remove(car)

        # add some lines to image
        start_point = (0, int( FRAME_HEIGHT * DETECTION_ZONE))
        end_point = ( int(FRAME_WIDTH) ,int( FRAME_HEIGHT * DETECTION_ZONE)) 
        cv2.line(ready_frame, start_point, end_point,(124,252,0), 10)

    #  ----------------------------------
    #   FPS
        FPS_counter += 1
        if time.time() - FPS_timer > 1:
            FPS_timer = time.time()
            FPS = FPS_counter
            FPS_counter = 0
        cv2.putText(ready_frame, str(FPS), (7, 70), cv2.FONT_HERSHEY_SIMPLEX , 3, GREEN, 3, cv2.LINE_AA) 
        cv2.imshow('frame',ready_frame)
    else: 
        first_go = False
        cv2.imshow('frame', frame)

    # Display the resulting frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # logger(str(car_list), LOG)
        logger('cars found: ' + str(len(car_list)), LOG)
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
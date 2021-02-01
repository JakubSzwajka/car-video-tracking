import threading
import traceback
import cv2
import time

import src.settings as settings
from src.Frame import Frame
from src.Tracker import Tracker
from src.utils import FPS, logger

import streamlit as st

def classifyWithYOLO():
    while True:

        global STOP_CLASSIFIER_THREAD 
        if STOP_CLASSIFIER_THREAD: 
            break

        print(f'{time.ctime()} Cars to check: ' + str(len(Tracker.objectsToClassify)))

        # take the oldest one 
        if len(Tracker.objectsToClassify) > 0:
            ObjectToClassify = Tracker.objectsToClassify[0]
            # verify it 
            ObjectToClassify.label = "Samochodzik"
            time.sleep(1)
            # remove from list 
            Tracker.objectsToClassify.remove(ObjectToClassify)
        else:
            time.sleep(0.5)

def runVideo( cap ):

    # streamWindow = st.empty()

    Frame.frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    Frame.frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    first_go = True
    frame = None
    current_frame = None
    previous_frame = None

    while(True):
        # testVar = st.slider('X')

        if first_go != True:
            previous_frame = Frame(current_frame.getFrame())
        
        ret, frame = cap.read()
        if ret == False: 
            break
        else:
            current_frame = Frame(frame)
        
        if first_go != True:

            difference_frame = current_frame.getDifferenceFrame(previous_frame)
            
            thresholded_frame = difference_frame.getBinary(threshold = 100)
            
            dilated_frame = thresholded_frame.getDilated( iterations = 10)
            
            valid_contours = dilated_frame.findObjects( minContourZone = settings.MIN_COUNTOUR_ZONE )
            Tracker.registerNewObjects(valid_contours, current_frame)

            # set which frame to display for user
            ready_frame = current_frame            
            
            ready_frame.addBoundingBoxesFromContours(Tracker)
            
            st.write("test")
            ready_frame.putText( "Threads: " + str(threading.active_count()), (7,20))
            ready_frame.putText( "Object Bufor size: " + str(len(Tracker.objectsToClassify)), (7,50))
            ready_frame.putText( "FPS: " + FPS.tick(), (7, 80)) 
            ready_frame.putText( "Cars passed: " + str(len(Tracker.lostObjects)), ( 7, 110))
            ready_frame.putText( "Test var: " + str(12), (7,140) )

            ready_frame.show()
        else: 
            first_go = False
            current_frame.show()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger('cars found: ' + str(Tracker.lostObjects), settings.LOG)
            break

    cap.release()
    cv2.destroyAllWindows()
    stopThreads()

def stopThreads():
    global STOP_CLASSIFIER_THREAD
    STOP_CLASSIFIER_THREAD = True

def main(video):
    global STOP_CLASSIFIER_THREAD    
    STOP_CLASSIFIER_THREAD = st.checkbox("Stop recognition", value=False, key=None)
    # STOP_CLASSIFIER_THREAD = False

    try:
        classifierThread = threading.Thread(target=classifyWithYOLO)
        classifierThread.start()

        runVideo(video)

    except Exception as e:
        # just in case to stop threads 
        print(traceback.format_exc())
        stopThreads()    

import time 
import cv2 
import imutils

def logger(message, if_log = True):
    if if_log: print(f'{time.ctime()}:', message)
    
def determinate_total_frames(video_path):

    vs = cv2.VideoCapture(video_path)
    # try to determine the total number of frames in the video file
    try:
        prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
            else cv2.CAP_PROP_FRAME_COUNT
        total = int(vs.get(prop))
        logger("{} total frames in video".format(total))
    # an error occurred while trying to determine the total
    # number of frames in the video file
    except:
        logger("could not determine # of frames in video")
        logger("no approx. completion time can be provided")
        total = -1

    return total


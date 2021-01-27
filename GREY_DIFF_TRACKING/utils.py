import time
import cv2 

class FPS:
    FPS_counter = 0
    FPS_timer = 0
    fps = 0

    def tick():
        FPS.FPS_counter += 1
        if time.time() - FPS.FPS_timer > 1:
            FPS.FPS_timer = time.time()
            FPS.fps = FPS.FPS_counter
            FPS.FPS_counter = 0
        return str(FPS.fps)


def logger( message, log = False):
    if log: print(f'{time.ctime()}', message)

def read_video( path ):
    cap = cv2.VideoCapture(path)
    if cap.isOpened():
        logger('Video: ' + path + ' opened')
    else:
        raise Tracking_Exception('File not found')
    return cap
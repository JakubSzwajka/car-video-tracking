from src.program import main
from src.utils import readVideo

from urllib.request import urlopen
import http.client
import time 

VIDEO_PATH = 'videos/droga.mp4'

if __name__ == "__main__":
    # videoCapture = readVideo(VIDEO_PATH)
    # main(videoCapture)

    tstart = time.time()

    conn = http.client.HTTPSConnection('998c906c02bb.ngrok.io')
    print('stworzenie klienta: ' ,time.time() - tstart)
    t1 = time.time()
    conn.request("GET", "/")
    response = conn.getresponse()
    print('Request 1: ', time.time() - t1)

    print(response.status, response.reason)
    print(response.read())

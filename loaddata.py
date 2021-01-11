import argparse
import imutils
from imutils.video import VideoStream
import cv2
import os
import time
import copy
import numpy as np
import timeit

ap=argparse.ArgumentParser()
ap.add_argument("-c","--cascade",required=True,
                help="path to cascade detector")
ap.add_argument("-0","--output",required=True,
                help="path to output")
args=vars(ap.parse_args())
detector=cv2.CascadeClassifier(args["cascade"])
#vs = VideoStream(src=0).start()
print("[INFO] starting video stream...")
url = "http://192.168.1.61:4747/video"
vs = VideoStream(url).start()
time.sleep(2.0)
total = 0
while True:
    frame = vs.read()
    orig = frame.copy()
    frame = imutils.resize(frame, width=400)
    rects=detector.detectMultiScale(
		cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1,
		minNeighbors=5, minSize=(30, 30))
    for (x,y,W,H) in rects :
        cv2.rectangle(frame,(x,y),(x+W,y+H),(0,255,0),2)
        cv2.imshow("Frame",frame)
        roi = frame[y:y + H, x:x + W]
        key=cv2.waitKey(1)&0xFF
    # if key == ord("k"):
    #     p = os.path.sep.join([args["output"], "{}.png".format(
    #         str(total).zfill(5))])
    #     cv2.imwrite(p, roi)
    #     total +=1
    if key==ord("p"):
        p = os.path.sep.join([args["output"], "{}.png".format(str(total).zfill(5))])
        cv2.imwrite(p, frame)
        total += 1
    elif key==ord("q"):
            break
print("face images stored".format(total))
print("cleaning up...")
cv2.destroyAllWindows()
vs.stop()
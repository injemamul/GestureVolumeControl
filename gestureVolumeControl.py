import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from subprocess import call
#######################################

'''

valid = False

while not valid:
    volume = 50

    try:
        volume = int(volume)

        if (volume <= 100) and (volume >= 0):
            call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
            valid = True

    except ValueError:
        pass
        
'''

minVol = 0
maxVol = 100


#######################################
wCam, hCam = 640, 480
#######################################

cap = cv2.VideoCapture('/home/kaish/MLprojects/HandTrackingProject/videos/VolControl.mp4')
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)
volBar = 400
vol = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        cv2.circle(img, (x1, y1), 4, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 4, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand Range 30-250
        # Volume Range 0-100

        vol = np.interp(length, [30, 250], [minVol, maxVol])
        volBar = np.interp(length, [30, 250], [400, 150])
        print(vol)

        try:
            if (vol <= 100) and (vol >= 0):
                call(["amixer", "-D", "pulse", "sset", "Master", str(vol) + "%"])
                valid = True

        except ValueError:
            pass



        if length<50:
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85,400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'Volume: {int(vol)} %', (30, 420), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (30, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    cv2.imshow("img", img)
    cv2.waitKey(1)
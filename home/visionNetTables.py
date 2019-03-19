import cv2
import numpy as np
import time
import asyncio
from networktables import NetworkTables
import logging
#grip.py
import gripnewmon as grip

import os
import fnmatch

DEBUG = True

logging.basicConfig(level=logging.DEBUG)


def transmit(gripPipe,camera, NetTable):
    res, frame = camera.read()
    if frame is None:
      print("No frame received!")
      print("Check your video device and try again")
      exit()


    x1 = None
    y1 = None
    w1 = None
    
    x2 = None
    y2 = None
    w2 = None
    contourList = []
    
    gripPipe.process(frame);
    if gripPipe.filter_contours_output: # if it found stuff
       for contour in gripPipe.filter_contours_output:
          #print("a")
          rect = cv2.boundingRect(contour)
          X = rect[0] + (rect[2] / 2)
          Y = rect[1] + rect[3]
          W = rect[2]
          #print("A"+numStr+" = "+str(cv2.contourArea(contour)))
          #print("X"+numStr+" = "+str(X))
          #print("Y"+numStr+" = "+str(Y))
          #print("W"+numStr+" = "+str(W))
          contourList.append(contour)
       #print(len(contourList))
       if len(contourList) == 2:
         R = None
         AL = None
         contour1 = contourList[0]
         contour2 = contourList[1]
         a1 = cv2.contourArea(contour1)
         a2 = cv2.contourArea(contour2)
         rect1 = cv2.boundingRect(contour1)
         rect2 = cv2.boundingRect(contour2)
         x1 = rect1[0] + (rect1[2] /2)
         x2 = rect2[0] + (rect2[2] /2)
         
         if x1 > x2:
           R = a1 / a2
           AL = a1
         else:
           R = a2 / a1
           AL = a2
         R = round(R, 3) # round the ratio so we dont get a super long float
         CenterX = (x1 + x2) / 2
         print("AL = "+str(AL))
         print("R = "+str(R))
         print("X1 = "+str(x1))
         print("X2 = "+str(x2))
         print("CX = "+str(CenterX))
         

         NetTable.putNumber("AL", AL);
         NetTable.putNumber("R", R);
         NetTable.putNumber("X1", x1);
         NetTable.putNumber("X2", x2);
         NetTable.putNumber("CX", CenterX);

       else:
         NetTable.putNumber("AL", -1);
         NetTable.putNumber("R", -1);
         NetTable.putNumber("X1", -1);
         NetTable.putNumber("X2", -1);
         NetTable.putNumber("CX", -1);

       rect1 = cv2.boundingRect(gripPipe.filter_contours_output[0])
       x1 = rect1[0] + (rect1[2] /2)
       y1 = rect1[1] + rect1[3]
       w1 = rect1[2]
       
       #rect2 = cv2.boundingRect(gripPipe.filter_contours_output[1])
       #x2 = rect2[0] + (rect2[2] /2)
       #y2 = rect2[1] + rect2[3]
       #w2 = rect2[2]
     
    if DEBUG == True:
       cv2.imshow("Debug", frame) #,mask)
       cv2.waitKey(1)

    print("-----")
    if False: #x1
      print("X1 = "+str(x1))
      print("Y1 = "+str(y1))
      print("W1 = "+str(w1)) # when do we need this?

    if False:
      print("X2 = "+str(x2))
      print("Y2 = "+str(y2))
      print("W2 = "+str(w2))
      
      NetTable.putNumber("X", x1);
      NetTable.putNumber("Y", y1);
      NetTable.putNumber("W", w1);

# by calling vdevice.set(<proberty num>, value)
#0 = POS_MSEC Current position of the video file in milliseconds.
#1 = POS_FRAMES 0-based index of the frame to be decoded/captured next.
#2 = POS_AVI_RATIO Relative position of the video file
#3 = FRAME_WIDTH Width of the frames in the video stream.
#4 = FRAME_HEIGHT Height of the frames in the video stream.
#5 = FPS Frame rate.
#6 = FOURCC 4-character code of codec.
#7 = FRAME_COUNT Number of frames in the video file.
#8 = FORMAT Format of the Mat objects returned by retrieve() .
#9 = MODE Backend-specific value indicating the current capture mode.
#10 = BRIGHTNESS Brightness of the image (only for cameras).
#11 = CONTRAST Contrast of the image (only for cameras).
#12 = SATURATION Saturation of the image (only for cameras).
#13 = HUE Hue of the image (only for cameras).
#14 = GAIN Gain of the image (only for cameras).
#15 = EXPOSURE Exposure (only for cameras).
#16 = CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
#17 = WHITE_BALANCE Currently unsupported
#18 = RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)
def CV_BRIGHTNESS_PROP(): return 10
def CV_FPS_PROP(): return 5

#Find the camera device number
#Should look like /dev/video0, where 0 is the camera number
#TODO determine the vision camera from the list of cameras in the dev folder

videoNum = None
for file in os.listdir('/dev'):
  if fnmatch.fnmatch(file, 'video[0-9]'):
     videoNum = int(file[-1:])
     break

if not videoNum is None:
  vdevice = cv2.VideoCapture(videoNum)         #configure the camera device
  vdevice.set(CV_FPS_PROP(), 60)
  vdevice.set(CV_BRIGHTNESS_PROP(), 0.3)
else:
  print("Failed to find camera")
  exit()
time.sleep(2)                     #give the camera a second to power on

g = grip.GripPipeline()
NetworkTables.initialize(server='10.21.58.2')
nt = NetworkTables.getTable("SmartDashboard")

while True:
    transmit(gripPipe=g,camera=vdevice, NetTable=nt)

    



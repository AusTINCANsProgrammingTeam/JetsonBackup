import cv2
import numpy as np
import time
import asyncio
import websockets
from networktables import NetworkTables
import logging
#grip.py
import grip

import os
import fnmatch

DEBUG = False

logging.basicConfig(level=logging.DEBUG)


def transmit(gripPipe,camera, NetTable):
    res, frame = camera.read()
    if frame is None:
      print("No frame received!")
      print("Check your video device and try again")
      exit()


    x = None
    y = None
    w = None
    gripPipe.process(frame);
    if gripPipe.filter_contours_output:
       r = cv2.boundingRect(gripPipe.filter_contours_output[0])
       x = r[0] + (r[2] /2)
       y = r[1] + r[3]
       w = r[2]
     
    if DEBUG == True:
       cv2.imshow("idklol", frame) #,mask)
       cv2.waitKey(1)


    if x:
#      print("X = "+str(x))
#      print("Y = "+str(y))
#      print("W = "+str(w))
      
      NetTable.putNumber("X", x);
      NetTable.putNumber("Y", y);
      NetTable.putNumber("W", w);
    else:
      NetTable.putNumber("X", -1);
      NetTable.putNumber("Y", -1);
      NetTable.putNumber("W", -1);
      #print("None found!")


# These are the different camera proberties that can be set
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
#TODO expand for multiple cameras

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

g = grip.GripPipelineLine()
NetworkTables.initialize(server='10.21.58.2')
nt = NetworkTables.getTable("SmartDashboard")

while True:
    transmit(gripPipe=g,camera=vdevice, NetTable=nt)

    



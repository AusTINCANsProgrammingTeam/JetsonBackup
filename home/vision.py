import cv2
import numpy as np
import time
import asyncio
import websockets

#grip.py
import grip

import os
import fnmatch

DEBUG = True

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

async def transmit(websocket,path):
  b = 0.1 
  while True:
    res, frame = vdevice.read()
    if frame is None:
      print("No frame received!")
      print("Check your video device and try again")
      #break

  #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #cv2.imshow("XD",frame)
    #cv2.waitKey(0)

    x = None
    y = None
    g.process(frame);
    if g.filter_contours_output:
       r = cv2.boundingRect(g.filter_contours_output[0])
       x = r[0] + (r[2] /2)
       y = r[1] + r[3]
       z = r[2]
     
    #lower_red = np.array([0,0,0])
    #upper_red = np.array([255,255,255])
    #mask = cv2.inRange(frame,lower_red,upper_red)
    if DEBUG == True:
       cv2.imshow("idklol", frame) #,mask)
       cv2.waitKey(1)
    #contours = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #websocket.send(contours)
    #contours = np.array(contours)
    #contours = sorted(contours,key=cv2.contourArea, reverse=True)[:1]

    if x:
      #M = cv2.moments(contours[0])
      #cx = int(M['m10']/M['m00'])
      #cy = int(M['m01']/M['m00'])
      print("X = "+str(x))
      print("Y = "+str(y))
      print("Z = "+str(z))
    #async def transmit(websocket,path):
    #  #name = await websocket.recv()
      await websocket.send("X="+str(x)+" Y="+str(y))

    #asyncio.get_event_loop().run_until_complete(start_server)
    #asyncio.get_event_loop().run_forever()


    #else:
    #  print("None found!")
start_server = websockets.serve(transmit, '10.21.58.18', 2159)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



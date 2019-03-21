#!/bin/bash

#activate all cores
export PATH=$PATH:/usr/local/cuda-8.0/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-8.0/lib64:
echo 1 > /sys/devices/system/cpu/cpu2/online
echo 1 > /sys/devices/system/cpu/cpu1/online

./cameraFinder.sh

echo nvidia | sudo -S ifconfig wlan0 down 

python3 ./visionNetTables.py &

cd /home/nvidia/Desktop/JetsonCameras-master/mjpg-streamer-experimental
declare -i var=0

while var < 5
do
   d=$(date +%Y%m%d%H%M%S)
   #echo $d
   python3 ./start.py
   var = $var+1
done

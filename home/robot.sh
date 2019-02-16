#!/bin/bash

while true
do
   d=$(date +%Y%m%d%H%M%S)
   #echo $d
   stdbuf -oL python3 /home/nvidia/visionNetTables.py > /home/nvidia/RobotLogs/"$d"_robot_stdOut.log 2> /home/nvidia/RobotLogs/"$d"_robot_stdErr.log
done

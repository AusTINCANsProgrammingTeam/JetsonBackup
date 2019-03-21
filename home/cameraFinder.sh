#!/bin/bash

dir=$(pwd)
rm -f cameraMap.txt
for i in $(ls /dev/video*)
do
	cd -P $(ls -l $i | awk -F'[,\ ]'  '{print "/sys/dev/char/"$5":"$7"/../../.."}')
	productID=$(cat idProduct)
        cd $dir
	echo "$i $productID" >> cameraMap.txt
done



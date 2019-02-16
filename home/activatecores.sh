export PATH=/usr/local/cuda-8.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/u$
export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64:
echo 1 > /sys/devices/system/cpu/cpu2/online
echo 1 > /sys/devices/system/cpu/cpu1/online

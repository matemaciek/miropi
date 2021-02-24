#!/usr/bin/env bash

cd /home/pi/miropi/zero
python3 main.py
RES=$?
while [ $RES == 42 ]
do
    python3 main.py
    RES=$?
done
if [ $RES == 0 ]
then
    sudo shutdown -h now
fi
if [ $RES == 21 ]
then
    sudo reboot
fi

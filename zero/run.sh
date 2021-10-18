#!/usr/bin/env bash

cd /home/pi/miropi/zero

#TODO: make this a part of fbcp service stop
raspi-gpio set 8 op
raspi-gpio set 10,11 a0

python3 main.py
RES=$?

if [ $RES == 42 ]
then
    sudo shutdown -h now
fi
if [ $RES == 21 ]
then
    sudo reboot
fi

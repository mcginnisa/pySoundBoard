#!/bin/bash
sudo chmod 4755 /sbin/shutdown #this will allow the program to shutdown  the pi

apt install python3-xlrd -y #installing dependencies
apt install python3-pygame -y

# create autostart file
mkdir /home/pi/.config/autostart
cp raspi_soundboard.py /home/pi/.config/autostart/soundboard.desktop
chmod 777 /home/pi/.config/autostart/soundboard.desktop

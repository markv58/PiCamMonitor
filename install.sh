#!/usr/bin/env bash

pip3 install -r requirements.txt --user
cp -a ~/.polyglot/nodeservers/PiCamMonitor/ScriptTemplates/. ~/.polyglot/nodeservers/PiCamMonitor/Scripts/
sudo chmod +x -R ~/.polyglot/nodeservers/PiCamMonitor/Scripts # activate the scripts
mkdir /home/pi/Pictures/Family
mkdir /home/pi/Pictures/Friends
mkdir /home/pi/Pictures/Kids
mkdir /home/pi/Pictures/Vacation
mkdir /home/pi/Pictures/Christmas
mkdir /home/pi/Pictures/Valentines
mkdir /home/pi/Pictures/StPatricks
mkdir /home/pi/Pictures/Easter
mkdir /home/pi/Pictures/YomKippur
mkdir /home/pi/Pictures/Halloween
mkdir /home/pi/Pictures/Thanksgiving
mkdir /home/pi/Pictures/NewYears
mkdir /home/pi/Pictures/Birthday1
mkdir /home/pi/Pictures/Birthday2
mkdir /home/pi/Pictures/Birthday3
mkdir /home/pi/Pictures/Birthday4
mkdir /home/pi/Pictures/Birthday5
mkdir /home/pi/Pictures/User1
mkdir /home/pi/Pictures/User2
mkdir /home/pi/Pictures/User3
mkdir /home/pi/Pictures/User4
sleep 2s
find /home/pi/Pictures -type d -exec cp -i /home/pi/.polyglot/nodeservers/PiCamMonitor/Images/sample.jpg {} \;


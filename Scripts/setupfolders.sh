#!/usr/bin/env bash

#make the directories for PictureFrame and copy sample.jpg there, does not alter existing dirs.

case "$1" in # this is for the normal first install of PictureFrame folders and sample.jpg
  normal)
    git config core.filemode false
    cmd_output=$(unam -o)
    if [ "$cmd_outut" == "FreeBSD" ]; then
      echo "Can't install on this system"
      exit
    fi
    if [ ! -d "/home/pi/Pictures/Family" ]; then
      echo "Setting up the folders"
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
      find /home/pi/Pictures -type d -exec cp -n /home/pi/.polyglot/nodeservers/PiCamMonitor/Images/sample.jpg {} \;
    else
      echo "Folders are already set up"
    fi
    ;;
  force) # this will force install PictureFrame folders and sample.jpg
    echo "Setting up the folders by force"
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
    find /home/pi/Pictures -type d -exec cp -n /home/pi/.polyglot/nodeservers/PiCamMonitor/Images/sample.jpg {} \;
    ;;  
*)
exit 1
;;

esac   

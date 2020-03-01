#!/bin/bash
### BEGIN INIT INFO
# Provides: omxplayer
### END INIT INFO

# Camera Feeds & Positions Quad
top_left="screen -dmS stream2 sh -c 'omxplayer --win \"0 0 400 240\" "$2" -b --live; exec bash'"
top_right="screen -dmS stream3 sh -c 'omxplayer --win \"400 0 800 240\" "$3" --live; exec bash'"
bot_left="screen -dmS stream4 sh -c 'omxplayer --win \"0 240 400 480\" "$4" --live; exec bash'"
bot_right="screen -dmS stream5 sh -c 'omxplayer --win \"400 240 800 480\" "$5" --live; exec bash'"
# Triple
main_left1="screen -dmS stream2 sh -c 'omxplayer --win \"0 90 500 390\" "$2" -b --live; exec bash'"
top_right1="screen -dmS stream3 sh -c 'omxplayer --win \"500 60 800 240\" "$3" --live; exec bash'"
bot_right1="screen -dmS stream4 sh -c 'omxplayer --win \"500 240 800 420\" "$4" --live; exec bash'"
# Double1
left1="screen -dmS stream2 sh -c 'omxplayer --win \"0 120 400 360\" "$2" -b --live; exec bash'"
right1="screen -dmS stream3 sh -c 'omxplayer --win \"400 120 800 360\" "$3" --live; exec bash'"
# Double2
left2="screen -dmS stream2 sh -c 'omxplayer --win \"0 120 400 360\" "$2" -b --live; exec bash'"
right2="screen -dmS stream3 sh -c 'omxplayer --win \"400 120 800 360\" "$3" --live; exec bash'"
# Single
full_screen1="screen -dmS stream2 sh -c 'omxplayer --win \"0 0 800 480\" "$2" -b --live; exec bash'"

# Camera Feed Names
camera_feeds_quad=(top_left top_right bot_left bot_right)
camera_feeds_triple=(main_left1 top_right1 bot_right1)
camera_feeds_double1=(left1 right1)
camera_feeds_double2=(left2 right2)
camera_feeds_single1=(full_screen1)

# Assign cameras
case "$1" in
  cams4x)
    for i in "${camera_feeds_quad[@]}"
    do
    eval eval '$'$i
    done
    ;;
  cams3x)
    for i in "${camera_feeds_triple[@]}"
    do
    eval eval '$'$i
    done
    ;;
   cams2x1)
    for i in "${camera_feeds_double1[@]}"
    do
    eval eval '$'$i
    done
    ;;
  cams2x2)
    for i in "${camera_feeds_double2[@]}"
    do
    eval eval '$'$i
    done
    ;;
  camera1)
    for i in "${camera_feeds_single1[@]}"
    do
    eval eval '$'$i
    done
    ;;
  pictureFrame)
    DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority /usr/bin/feh -q -p -z -Z -F -R  60 -Y -D "$2" "$3"
    ;;
  sb)
    DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority /usr/bin/feh -q -Z -F -Y /home/pi/.polyglot/nodeservers/PiCamMonitor/Images/blank.png
    ;;    
  on)
    echo 0 | sudo tee /sys/class/backlight/rpi_backlight/bl_power
    ;;
  off)
    echo 1 | sudo tee /sys/class/backlight/rpi_backlight/bl_power
    ;;
  pkill)
    sudo pkill feh
    ;; 
  mkill)
    screen -X -S stream1 quit
    ;;
  omxkill)
    screen -X -S stream2 quit
    screen -X -S stream3 quit
    screen -X -S stream4 quit
    screen -X -S stream5 quit
    ;;
  killall)
    killall screen -q
    ;;
  shutDownPi)
    sudo shutdown -h now
    ;;
  rebootPi)
    sudo reboot
    ;;
  MMstart)
    cd ~/MagicMirror
    # unclutter -display :0 -idle 3 -root -noevents
    sleep 1s
    screen -dmS stream1 sh -c 'DISPLAY=:0 npm start; exec bash'
    ;;
  unclutter)
    unclutter -display :0 -idle 3 -root -noevents
    ;;
  ''|*[0-9]*)
    echo "$1" | sudo tee /sys/class/backlight/rpi_backlight/brightness
    ;;

*)
exit 1
;;

esac

#!/usr/bin/env bash

case "$1" in
  normal)
    cmd_output=$(uname -o)
    if [ "$cmd_output" == "FreeBSD" ]; then
      echo "Can't install on this system"
      exit
    fi
    if [ ! -d "/home/pi/MagicMirror" ]; then
      echo "MagicMirror2 is not installed"
      exit
    else
      echo "MagicMirror2 is installed"
    fi

    if [ -e "/home/pi/MagicMirror/config/config.js" ]; then
      echo "The MagicMirror2 files are already installed"
      exit
    else
      cp ~/.polyglot/nodeservers/PiCamMonitor/Files/config.js ~/MagicMirror/config/
      cp ~/.polyglot/nodeservers/PiCamMonitor/Files/custom.css ~/MagicMirror/css/
      cp ~/.polyglot/nodeservers/PiCamMonitor/Files/main.css ~/MagicMirror/css/
      mkdir ~/MagicMirror/modules/Pictures
      cp ~/.polyglot/nodeservers/PiCamMonitor/Images/sample.jpg /home/pi/MagicMirror/modules/Pictures/
      echo "The MagicMirror2 files have been installed"
    fi
    ;;
  force)
    cp ~/.polyglot/nodeservers/PiCamMonitor/Files/config.js ~/MagicMirror/config/
    cp ~/.polyglot/nodeservers/PiCamMonitor/Files/custom.css ~/MagicMirror/css/
    cp ~/.polyglot/nodeservers/PiCamMonitor/Files/main.css ~/MagicMirror/css/
    mkdir ~/MagicMirror/modules/Pictures
    cp ~/.polyglot/nodeservers/PiCamMonitor/Files/sample.jpg /home/pi/MagicMirror/modules/Pictures/
    echo "The MagicMirror2 files have been installed"
    ;;

*)
exit 1
;;

esac

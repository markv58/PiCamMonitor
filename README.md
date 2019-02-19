# PiCamMonitor
This is a polyglot nodeserver for UDI Isy that runs on a Raspberry Pi 3 B+ with the official 7" RPi touch screen in a SmartiPi Touch case.
This is a stand alone unit for displaying your ip surveillance camera feeds in a single or multiple feed configuration. Feeds can be displayed using ISY events, maually or with smart home devices such as Alexa through the ISY portal.

There is a Picture Frame option to diplay your photos when the unit is not displaying camera feeds that can be programmed to run only during certain times or all the time. Various folder options allow you to have different themes, Christmas, Birthdays, Halloween, Kids, Favorites, etc., that can be run during certain seasons or on certain days.

If you are running the Presence-Poly nodeserver you can also run one on this unit. I expect that there will be further enhancements in the future.

# Installation

### HARDWARE:

* Raspberry Pi 3 B+
* 5.2 vdc 3 amp power supply, I've found the 2.5 amp to be too weak to power the Pi and screen.
* 16 - 32 GB micro sd card
* Official Raspberry Pi 7" touch screen 
* SmartiPi Touch Case* - https://smarticase.com available on Amazon.com

### OPTIONAL:

* Piezo buzzer - https://www.amazon.com/Cylewet-Mainboard-Computer-Internal-Speaker/dp/B01MR1A4NV/ref=sr_1_1_sspa?s=electronics&ie=UTF8&qid=1550533551&sr=1-1-spons&keywords=piezo+buzzer&psc=1 I realize there are 10, but they are cheap and once you get one of these running, you may just want a few more.
* Heatsinks - 

Assemble the Smarti Pi case, screen and raspberry pi, instructions and video here - https://smarticase.com/products/smartipi-touch .

Download the full version of Raspbian Stretch with Desktop and recommended software found here - https://www.raspberrypi.org/downloads/raspbian/ .
Extract the files.

Using Etcher (Mac) https://www.balena.io/etcher/ , or
Win32DiskManager (PC) https://sourceforge.net/projects/win32diskimager/ , image the micro sd card.
After imaging, insert the sd card into the pi, replace the cover, plug in a usb mouse and keyboard and power up. The mouse and keyboard are only needed for the initial set-up.

You will be presented with the Welcome screen.

Follow the promts to set up your device, connect to your wifi and then update the software. (This will take a while)

While you wait for the Pi to update, you may want VNC viewer installed on your main computer. https://www.realvnc.com/en/connect/download/viewer/ You might find it useful to install the VNC viewer on an iPad or other tablet.

When the updates have been installed, click OK and then reboot. Click the raspberry in the top left corner and select Preferences/Raspberry Pi Configuration.

On the first page select Wait for Network. Select Interfaces tab and check SSH and VNC enable. Select Performance tab and change the GPU memory to 256. Click OK then YES to reboot.

Set a static ip address. Depending on your system there are various way to achieve this. On the Pi itself, open the terminal window and enter 'sudo nano /etc/dhcpcd.conf' , hit enter and scroll to the bottom.

Enter (editing the ip numbers to match your network configuration, eth0=wired, wlan0=wireless):

    interface eth0

    static ip_address=192.168.0.10/24
    static routers=192.168.0.1
    static domain_name_servers=192.168.0.1
    
    interface wlan0
    
    static ip_address=192.168.0.200/24
    static routers=192.168.0.1
    static domain_name_servers=192.168.0.1

Exit the editor, press ctrl+x, press the letter 'Y' then enter. Note your ip address and 
type 'sudo reboot' and hit enter for the changes to take affect. 
You can now move to VNC, ssh or continue with the mouse and keyboard.

Next we need to stop the screen from blanking after 10 minutes. In the terminal enter 'sudo apt-get install xscreensaver' then hit enter. Once all the files are installed and you are back to the prompt, type 'sudo reboot' and hit enter. When the Pi is back up to the desktop select the raspberry/Preferences/Screensaver and set the Mode: to Disable Screen Saver and close the window. Now the screen should stay on like we want.

Set up Samba so you can transfer your pictures, in the terminal enter 'sudo apt-get install samba samba-common-bin' and hit enter. Back at the prompt enter: 'sudo nano /etc/samba/smb.conf' and hit enter. Scroll to the very bottom and enter:

    [global]

    workgroup = workgroup 
    server string = %h  
    wins support = no
    dns proxy = no
    security = user
    map to guest = Bad User
    encrypt passwords = yes
    panic action = /usr/share/samba/panic-action %d
  

    [Home]

    comment = Home Directory
    path = /home/pi
    browseable = yes
    writeable = yes
    guest ok = yes
    read only = no
    force user = root
  
Again, press ctrl+x hit 'Y' then enter to save the file. Enter: 'sudo samba restart' enter for the changes to take effect. When you connect from your computer, log in as guest and copy your pictures to the appropriate folder under the Pictures folder.
  
Two more quick installs and we are ready for Polyglot.
* Install screen: sudo apt-get install screen
* Install feh: sudo apt-get install feh

Install polyglot: wget -qO - https://raw.githubusercontent.com/UniversalDevicesInc/polyglot-v2/master/scripts/install.sh | bash -e

Set up the Polyglot. You got this now.

(It's not a bad idea to backup your ISY at this point, really, do it just in case.)

#### Install PiCamMonitor, get it from the Node Store or manualy here: https://github.com/markv58/PiCamMonitor.git

Manualy: 

1. cd .polyglot/nodeservers
2. git clone https://github.com/markv58/PiCamMonitor.git 
3. cd PiCamMonitor 
4. chmod +x install.sh 
5. ./install.sh <enter>
 
Install the Nodeserver

# Camera Feeds and Paths

With high resolution cameras you will use the sub stream, the higher resolutions will not play properly. Log into your camera through a web brower and make sure your sub stream is enabled, set to 640x480 and the highest frame rate. Set the key frame to twice the max frame rate. This will make your streams load faster.

A lower resolution camera like the Foscam C1, which is still 720p can be streamed from the main feed.

A typical path to the sub feed of a high quality camera. (Amcrest and others in the range)\(PLEASE NOTE the backslash between the 1 and the &, this is a requirement if there is an ampersand in your path)

    rtsp://user:password@192.192.192.195:544/cam/realmonitor?chanel=1\&subtype=1 


A typical path to the main stream on lower end camera such as a Foscam C1.

    rtsp://user:password@192.192.192.192:544/videoMain 


You can search the web for the settings to reach your particular camera.

#### Test your camera feed paths on the Pi using this command line edited with your information:

    sh -c 'omxplayer --win "0 0 800 480" rtsp://USERNAME:PWORD@172.16.2.110:554/cam/realmonitor?channel=1\&subtype=1; exec bash'
This will run the sub stream on an Amcrest and most other high resolution cameras. If you are successful, save your feed path for use in the custom configuration parameters. Use ctrl+c to stop the player.


#### cam1, cam2, cam3 and cam4 must be in the custom configuration parameters.
    Key        Value
    cam1       rtsp://user:password@192.192.192.195:544/cam/realmonitor?chanel=1\&subtype=1
    
If you have no cam# the value must be 'none'. Fill the camera paths from 1 to 4 for the best results. A single or multi camera feed will not play if there is no camera for the feed.

- cam2x1 plays cam1 and cam2 in 2 equal size windows
- cam2x2 plays cam3 and cam4 in 2 equal size windows
- cam3x plays three cams in a large main window and 2 smaller side windows, defaults to cam1, cam2 and cam3, can be changed in custom configuration parameters.
- cam4x plays all cams in 4 equal windows


# Custom Configuration Parameters

The PiCamMonitor will automatically start up and run a camera feed and the picture frame option using these settings. All input should be lower case.

* cam_screen_level = 0 - 250 (sets the default brightness of the camera feed, 130 default)
* cam_screen_timer = 10 - 120 (sets the default amount of time the feed will play, 20 seconds default)
* pic_frame_enable = true or false (enable the picture frame option, false default)
* pic_frame_auto = true or false (auto start the picture frame, false default)
* pic_screen_level = 0 - 250 (sets the default brightness of the picture frame, 130 default)
* pic_screen_timer = 10 - 120 (sets the default time a picture displays, 20 seconds default)
* pic_start_folder = 0 - 20 (sets the default picture folder, 0 default)
* screen_connected = true or false (safe guard to ensure you have a screen connected, false default)
* sound_on = true or false (default sound setting, false default)
* start_camera = 0 - 7 (sets the camera feed that plays at start up, 0 default)
* triple_feed1 The camera to display in the main panel
* triple_feed2 The camera to display in the top right panel
* triple_feed3 The camera to display in the bottom right panel. Any of the 4 cams, cam1 cam2 cam3 or cam4

### If you have any issues please visit the forums for assisance.

*I do not recommend the official Pi screen case. It was made wrong, the screen must be mounted upside down and requires a  configuration setting to flip the screen. This results in a terrible viewing angle.

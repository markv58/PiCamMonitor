# PiCamMonitor

#### v2.3.0 - Another Major, Major update.

You must check you configuration and update for proper operation. Clones must be updated also and cam feed information copied to or entered there.

After the update hit the Update Profile then restart the admin console to ensure you can access all features.

#### v2 - This is a major update, please read the Upgrade section below.

This is a Polyglot Nodeserver for UDI Isy that can run either as a controller on your local Polyglot to control clones or on a Raspberry Pi 3 B+ or 4 with the official 7" RPi touch screen in a SmartiPi Touch case. Running in stand alone mode gives you another instance of a Polyglot Nodeserver that you can install nodes onto such as the Presence-Poly.

This will display your ip surveillance camera feeds in a single or multiple feed configuration on the RPi. Feeds can be displayed using ISY events, Blue Iris alerts, maually or with smart home devices such as Alexa through the ISY portal.

There is a Picture Frame option to display your photos when the unit is not displaying camera feeds that can be programmed to run only during certain times or all the time. Various folder options allow you to have different themes, Christmas, Birthdays, Halloween, Kids, Favorites, etc., that can be run during certain seasons or on certain days.

An option to use MagicMirror2 for the display has been added. This will display your photos from a single directory only and adds a clock, the current weather and the weather forecast on the screen using the supplied configuration file. You can of course customize your MagicMirror display any way you like.


#### v2 - You can now have clones of a PiCamMonitor that will mirror the controller. This means you can have many around the house and only use a single node slot.

Clones must have the same options installed as the Controller if running in stand alone mode.  

The Short poll checks if the Clones are online and synchronized. If there is a problem with a clone the system will re-sync automatically.

## Upgrade from v2.04 to 2.3.0

Programs will be affected because the camera feeds from 2.0.3 have moved to the bottom of the list.
Sounds can be played through HDMI or the phone jack. A sound card can be added.

## Upgrade from v1.2.2

If you are upgrading to a stand alone unit install:

     sudo apt-get install unclutter

Set the screen resolution detailed in the Set Resolution section below.

Install MagicMirror as detailed in the MagicMirror installation section below.

If converting an existing PiCamMonitor to a clone see the section on Clones below.

# Installation of PiCamMonitor:

### If installing on a local Polyglot or Polisy to clontrol clones only, install from the NodeServer Store and skip to the Clones section below.

### HARDWARE:

* Raspberry Pi 3 B+ or 4
* 5.2 vdc 3 amp power supply for the 3 B+ or a 5.1 vdc 3 amp USB-C for the 4.
* 16 - 32 GB micro sd card
* Official Raspberry Pi 7" touch screen 
* SmartiPi Touch Case* - https://smarticase.com available on Amazon.com

### OPTIONAL Hardware:

* Sound card - https://www.amazon.com/gp/product/B07B3WYMN8/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1
* Piezo buzzer - https://www.amazon.com/Cylewet-Mainboard-Computer-Internal-Speaker/dp/B01MR1A4NV/ref=sr_1_1_sspa?s=electronics&ie=UTF8&qid=1550533551&sr=1-1-spons&keywords=piezo+buzzer&psc=1 I realize there are 10, but they are cheap and once you get one of these running, you may just want a few more. This connects to GPIO pins 9 thru 15 with the black wire on pin 9. https://pinout.xyz
* Heatsinks - 

Assemble the Smarti Pi case, screen and raspberry pi, instructions and video here - https://smarticase.com/products/smartipi-touch .

Download the full version of Raspbian Buster with Desktop found here - https://www.raspberrypi.org/downloads/raspbian/ .
Extract the files.

Using Etcher (Mac) https://www.balena.io/etcher/ , or
Win32DiskManager (PC) https://sourceforge.net/projects/win32diskimager/ , image the micro sd card.
After imaging, insert the sd card into the pi, replace the cover, plug in a usb mouse and keyboard and power up. The mouse and keyboard are only needed for the initial set-up.

You will be presented with the Welcome screen.

Follow the promts to set up your device, connect to your wifi and then update the software. (This will take a while) (If you encounter an error before the updates start just click Back and start again, it happens.)

While you wait for the Pi to update, you may want VNC viewer installed on your main computer. https://www.realvnc.com/en/connect/download/viewer/ You might find it useful to install the VNC viewer on an iPad or other tablet.

When the updates have been installed, click OK and then reboot. Click the raspberry in the top left corner and select Preferences/Raspberry Pi Configuration.

On the first page select Wait for Network. Select Interfaces tab and check SSH and VNC enable. Select Performance tab and change the GPU memory to 256. Click OK then YES to reboot.

Set a static ip address. Depending on your system there are various way to achieve this. On the Pi itself, open the terminal window and enter

    sudo nano /etc/dhcpcd.conf
    
hit enter and scroll to the bottom.

Enter (editing the ip numbers to match your network configuration, eth0=wired, wlan0=wireless):

    interface eth0

    static ip_address=192.168.0.10/24
    static routers=192.168.0.1
    static domain_name_servers=8.8.8.8 8.8.4.4
    
    interface wlan0
    
    static ip_address=192.168.0.200/24
    static routers=192.168.0.1
    static domain_name_servers=8.8.8.8 8.8.4.4

Note your ip address. Exit the editor, press ctrl+x, press the letter 'Y' then enter.

Enter:

    sudo reboot
    
and hit enter for the changes to take affect. 

You can now move to VNC, ssh or continue with the mouse and keyboard.

I've found it easier to cut and paste the commands using ssh and working with the Pi desktop using the VNC option.

### Set Resolution

This will make MagicMirror use the screen efficiently and gives you a better desktop resolution if you want to work
on some of the Pi settings like the screen saver and desktop settings.

    cd ~
    cd /boot
    sudo nano config.txt

Scroll down serveral lines and find the lines below and edit so that they are the same.

    # uncomment to force a console size. By default it will be display's size minus
    # overscan.
    framebuffer_width=1160
    framebuffer_height=700

Hit ctrl+x then 'Y' and enter to save the changes.

Reboot the Pi:

    sudo reboot

Setup your desktop preferences if you choose.

### Screensaver

Next we need to stop the screen from blanking after 10 minutes. In the terminal enter

    sudo apt-get install xscreensaver 
    
then hit enter. 

Once all the files are installed and you are back to the prompt it's time to run the screen saver and set it to disable.
Go to the desktop select the raspberry/Preferences/Screensaver and set the mode to Disable Screen Saver and close the window. You may be asked to start the service. Now the screen should stay on like we want.

### Samba

Set up Samba so you can transfer your pictures, in the terminal enter

    sudo apt-get install samba samba-common-bin
    
and hit enter. Back at the prompt enter

    sudo nano /etc/samba/smb.conf
    
and hit enter. Scroll to the very bottom and enter:

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
  
Again, press ctrl+x hit 'Y' then enter to save the file. Enter:

    sudo samba restart
    
then enter for the changes to take effect. When you connect from your computer, log in as guest and you can copy your pictures to the appropriate folder under the /home/pi/Pictures folder or to the /home/pi/MagicMirror/modules/Pictures folder that MagicMirror will use. The initial install will copy sample.jpg to every picture folder to avoid errors from choosing an empty folder. Delete that file when you populate the folder.
  
Three more quick installs and we are ready for MagicMirror2 and Polyglot. Enter the following, answer y if asked to let them install.

    sudo apt-get install screen
    sudo apt-get install feh
    sudo apt-get install unclutter

### MagicMirror installation:

Execute the following one at a time:

    cd ~
    curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
    sudo apt install -y nodejs

    git clone https://github.com/MichMich/MagicMirror
    cd MagicMirror
    npm install

⚠️ Important!

The installation step for npm install will take a few minutes, often with little or no terminal response! 
Do not interrupt or you risk locking up the system.

    cd modules
    git clone https://github.com/darickc/MMM-BackgroundSlideshow.git
    cd MMM-BackgroundSlideshow
    npm install

Ignore warnings.

#### You will need to register for and get an API key for the weather module:

    https://openweathermap.org

This will download the city list where you can find your location id:

    http://bulk.openweathermap.org/sample/city.list.json.gz

When you install PiCamMonitor configuration files will also be installed for MagicMirror. This will get you up and running quickly and you can modify the MagicMirror to suit your needs if you choose to.

Insert your weather module information in the configuration file after Polyglot and PiCamMonitor are installed:

    cd ~/MagicMirror/config
    nano config.js 

### Polyglot installation:

    cd ~
    wget -qO - https://raw.githubusercontent.com/UniversalDevicesInc/polyglot-v2/master/scripts/install.sh | bash -e

Set up the Polyglot. You got this now.

(It's not a bad idea to backup your ISY at this point, really, do it just in case.)

### PiCamMonitor installation, get it from the Node Store or manualy here: 

    https://github.com/markv58/PiCamMonitor.git

Manualy: 

    cd .polyglot/nodeservers
    git clone https://github.com/markv58/PiCamMonitor.git 
    cd PiCamMonitor 
    chmod +x install.sh 
    ./install.sh <enter>
 
Add the Nodeserver. Once PiCamMonitor starts you may need to restart it to populate the driver panels with current information.

### Camera Feeds and Paths setup and testing:

With high resolution cameras you will use the sub stream, the higher resolutions will not play properly. Log into your camera through a web brower and make sure your sub stream is enabled, set to 640x480 and the highest frame rate. Set the key frame to twice the max frame rate. This will make your streams load faster.

A lower resolution camera like the Foscam C1, which is still 720p can be streamed from the main feed.

A typical path to the sub feed of a high quality camera. (Amcrest and others in the range)\(PLEASE NOTE the backslash between the 1 and the &, this is a requirement if there is an ampersand in your path)

    rtsp://user:password@192.192.192.195:544/cam/realmonitor?chanel=1\&subtype=1 


A typical path to the main stream on lower end camera such as a Foscam C1.

    rtsp://user:password@192.192.192.192:544/videoMain 


You can search the web for the settings to reach your particular camera.

#### BlueIris Users:

You can stream your cameras from BlueIris. Please see the BI help files for additional settings information.

The path to your streams:

    http://user:password@xxx.xxx.xxx.xxx:port/mjpg/shortName\&stream=2
    

#### Test your camera feed paths on the Pi using this command line edited with your information:

    sh -c 'omxplayer --win "0 0 800 480" rtsp://USERNAME:PWORD@172.16.2.110:554/cam/realmonitor?channel=1\&subtype=1; exec bash'
This will run the sub stream on an Amcrest and most other high resolution cameras. If you are successful, save your feed path for use in the custom configuration parameters. Use ctrl+c to stop the player.


#### cam1, cam2, cam3 and cam4 must be in the custom configuration parameters.
    Key        Value
    cam1       rtsp://user:password@192.192.192.195:544/cam/realmonitor?chanel=1\&subtype=1
    
If you have no cam# the value must be 'none'. Fill the camera paths from 1 to 4 for the best results. A single or multi camera feed will not play if there is no camera for the feed.

- Cams 1+2 plays cam1 and cam2 in 2 equal size windows
- Cams 3+4 plays cam3 and cam4 in 2 equal size windows
- Cams x 3 plays three cams in a large main window and 2 smaller side windows, defaults to cam1, cam2 and cam3, can be changed in custom configuration parameters.
- Cams x 4 plays all cams in 4 equal windows

# Custom Configuration Parameters

After you have tested and entered your camera stream information, add the screen_connected true parameter and restart PiCamMonitor. After the restart you should see your cam1 stream for the default time.

The PiCamMonitor will automatically start up and run the feature option using these settings. All input should be lower case.

    stand_alone = true or false (false default, set to true if running on a RPi with the 7" official screen).
    
    mm_installed = true or false (false default, set to true if you have a working MagicMirror)

    cam_screen_level = 0 - 250 (sets the default brightness of the camera feed, 130 default)
    cam_screen_timer = 10 - 120 (sets the default amount of time the feed will play, 20 seconds default)
    
    clone1 = 192.192.192.195 (IP address) The key must start with 'clone' and each clone name must be unique.
    clone2 = 192.192.192.196 The key could be anything after 'clone'. clone_Bedroom, clone_Kitchen, cloneLR, etc.
    
    feature_auto_start = 0 - 2 (0 = Off, 1 = PictureFrame, 2 = MagicMirror, 0 default)
    feature_screen_level = 0 - 250 (sets the default brightness of the screen when running a feature, 130 default)

    pic_frame_timer = 10 - 120 (sets the default time a picture displays in the PictureFrame feature, 60 seconds default)
    pic_frame_folder = 1 - 21 (sets the default PictureFrame folder, 1 default)(Does not affect MagicMirror)

    sound_on = true or false (default sound setting, false default)

    triple_feed1 The camera to display in the main panel    << Only for a stand alone controller, will be ignored otherwise >>
    triple_feed2 The camera to display in the top right panel
    triple_feed3 The camera to display in the bottom right panel. Any of the 4 cams, cam1 cam2 cam3 or cam4

After changing or adding any parameter(s) and saving, restart the node.

After a restart, check the log for any errors. If you see a repeated connect disconnect, restart Polyglot to clear. You may need to re-fresh the page in order to see new log items.

# Clones

You can add clones to PiCamMonitor. Each of the clones will mirror the master and do not require a node slot.

Please go here for installation files and instructions:

   https://github.com/markv58/PCM-UDI-Clone

This is not available on the Nodeserver Store.

#### If you have any issues or questions, please visit the forums for assisance.

https://forum.universal-devices.com/topic/25817-polyglot-v2-picammonitor

*I do not recommend the official Pi screen case. It was made wrong, the screen must be mounted upside down and requires a  configuration setting to flip the screen. This results in a terrible viewing angle.

v1.2.4 Fixed some bugs, fixed install process.

v2.0.0 
* Clones can be added to expand the system without taking more node slots.
* Runs on local Polyglot without screens to control add on clones.
* MagicMirror2 can be used as a display Feature.
* Self healing if clones get out of sync.

v2.0.1 Fixed bug that would not allow sync process if a feature was not running. Fixed name.

v2.0.2 Compatible with Polisy

v2.0.3 Bugs fixed and preperation for future enhancements

v2.0.4 Bug fix that caused crash when running 4x feed

v2.3.0 Major update allows for any type of screen to be used with the master and clones with some limitations. Screen brightnes can't be controled on generic screen by PCM. There are more cameras allowed and Blue Iris group feeds are recommended. This version has a collection of custom sounds to announce alerts and a camera hold option to remain on a feed for an unlimited amount of time.

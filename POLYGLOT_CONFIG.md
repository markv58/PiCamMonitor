#### cam1, cam2, cam3 and cam4 must be in the custom configuration parameters to use the multi cam feeds.(Cams 1+2, Cams 2+4, etc)

A typical path to a camera feed:

    Key        Value
    cam1       rtsp://user:password@192.192.192.195:544/cam/realmonitor?chanel=1\&subtype=1
    
If you are running BlueIris software, you can get your streams from there:

    Key.       Value
    cam1       http://user:password@192.192.192.192:1234/mjpg/Cam1/video.mjpg\&stream=2
    
    bi_group1  http://user:password@192.192.192.192:1234/mjpg/@outside\&stream=2
    
On BlueIris you can set the stream preferences. See BI help section.

- Cams 1+2 plays cam1 and cam2 in 2 equal size windows
- Cams 3+4 plays cam3 and cam4 in 2 equal size windows
- Cams x 3 plays three cams in a large main window and 2 smaller side windows, defaults to cam1, cam2 and cam3, can be changed in custom configuration parameters.
- Cams x 4 plays all cams in 4 equal windows

The PiCamMonitor will automatically start up and run the feature option using these settings. Use lower case for all input.

    stand_alone = true or false (false default, set to true if running on a RPi with the 7" official screen).
    
    mm_installed = true or false (false default, set to true if you have a working MagicMirror install).
                                 (MagicMirror2 MUST be installed on all clones and on the stand-alone or setting)
                                 (this to true will cause some problems)
                                 
    clone1 = 192.192.192.192        Name and IP address of any clone, Key must start with clone.
    clone_LR = 192.192.192.193      The Key will be the name of the clone node in ISY.
    
    cam_screen_level = 0 - 250 (sets the default brightness of the camera feed, 130 default).
    cam_screen_timer = 10 - 120 (sets the default amount of time the feed will play, 20 seconds default).
    
    feature_auto_start = 0 - 2 (0 = Off, 1 = PictureFrame, 2 = MagicMirror, 0 default).
    feature_screen_level = 0 - 250 (sets the default brightness of the screen when running a feature, 50 default).
    
    pic_frame_timer = 10 - 120 (sets the default time a picture displays in the PictureFrame feature, 60 seconds default).
    pic_frame_folder = 1 - 21 (sets the default PictureFrame folder, 1 default)(Does not affect MagicMirror).
    
    sound = 0 - 17 (start up sound setting, 0 default).
    
    triple_feed1 The camera to display in the main window.                Any of the 4 cams
    triple_feed2 The camera to display in the top right windowl.       cam1 cam2 cam3 or cam4
    triple_feed3 The camera to display in the bottom right window. 

After changing or adding any parameter(s) and saving, restart the node.

#### When PictureFrame or MagicMirror starts for the first time after a stop or switch, the delay is normal.

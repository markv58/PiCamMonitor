The PiCamMonitor will automatically start up and run a camera feed and the picture frame option using these settings. All input should be lower case.

* cam__screen__level = 0 - 250 (sets the default brightness of the camera feed, 130 default)
* cam_screen_timer = 10 - 120 (sets the default amount of time the feed will play, 20 seconds default)
* pic_frame_enable = true or false (enable the picture frame option, false default)
* pic_frame_auto = true or false (auto start the picture frame, false default)
* pic_frame_level = 0 - 250 (sets the default brightness of the picture frame, 130 default)
* pic_frame_timer = 10 - 120 (sets the default time a picture displays, 20 seconds default)
* pic_frame_folder = 0 - 20 (sets the default picture folder, 0 default)
* screen_connected = true or false (safe guard to ensure you have a screen connected, false default)
* sound_on = true or false (default sound setting, false default)
* start_camera = 0 - 7 (sets the camera feed that plays at start up, 0 default)
* triple_feed1 The camera to display in the main panel
* triple_feed2 The camera to display in the top right panel
* triple_feed3 The camera to display in the bottom right panel. Any of the 4 cams, cam1 cam2 cam3 or cam4

After changing or adding any parameter(s) and saving, restart the node.

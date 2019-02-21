#!/usr/bin/env python3
"""
PiCamMonitor v1.2.1
This is a NodeServer for UDI Polyglot v2 that will display your ip camera sub-feeds on a 
Raspberry Pi 3 B+ with attached official 7" touch screen.
When not showing a camera feed an optional picture frame mode can display images from different folders.
"""
import polyinterface
import sys
import time
import os
import json
import subprocess
import threading
import gc

LOGGER = polyinterface.LOGGER
SPATH = "/home/pi/.polyglot/nodeservers/PiCamMonitor/Scripts/./"
STOPPER = None

# list of args to pass to displaycamera - Do Not Alter
CAM_SCRIPTS = ['camera1', #0
               'camera1', #1
               'camera1', #2
               'camera1', #3
               'cams2x1', #4
               'cams2x2', #5
               'cams3x',  #6
               'cams4x'   #7
              ]

# list of args to pass to pictureFrame - Do Not Alter
PICTURE_FOLDERS = ['/home/pi/Pictures/Family',       #0
                   '/home/pi/Pictures/Friends',      #1
                   '/home/pi/Pictures/Kids',         #2
                   '/home/pi/Pictures/Vacation',     #3
                   '/home/pi/Pictures/Christmas',    #4
                   '/home/pi/Pictures/Valentines',   #5
                   '/home/pi/Pictures/StPatricks',   #6
                   '/home/pi/Pictures/Easter',       #7
                   '/home/pi/Pictures/YomKippur',    #8
                   '/home/pi/Pictures/Halloween',    #9
                   '/home/pi/Pictures/Thanksgiving', #10
                   '/home/pi/Pictures/NewYears',     #11
                   '/home/pi/Pictures/Birthday1',    #12
                   '/home/pi/Pictures/Birthday2',    #13
                   '/home/pi/Pictures/Birthday3',    #14
                   '/home/pi/Pictures/Birthday4',    #15
                   '/home/pi/Pictures/Birthday5',    #16
                   '/home/pi/Pictures/User1',        #17
                   '/home/pi/Pictures/User2',        #18
                   '/home/pi/Pictures/User3',        #19
                   '/home/pi/Pictures/User4'         #20
                  ]

class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super().__init__(polyglot)
        self.name = 'PiCamMonitor'
        self.script_running = False
        self.timer_running = False
        self.picFrameRunning = False
        self.runTheFeed = True        
        self.cam2x1feed = False
        self.cam2x2feed = False
        self.cam3xfeed = False
        self.cam4xfeed = False        
        self.cam1 = 'none'
        self.cam2 = 'none'
        self.cam3 = 'none'
        self.cam4 = 'none'
        self.screenLevel = 130
        self.cam_screen_timer = 20
        self.picFrameAuto = False        
        self.picFrameEnable = False        
        self.pfscreenLevel = 130
        self.pic_screen_timer = 20
        self.screenConnected = False
        self.sound = False
        self.start_Camera = 0
        self.pfFolder = 0
        self.cam3x_feed1 = self.cam1
        self.cam3x_feed2 = self.cam2
        self.cam3x_feed3 = self.cam3
                                   
    def start(self):
        LOGGER.info('Started PiCamMonitor')
        self.check_params()
        self.setOn()
        self.query()

    def shortPoll(self):
        pass

    def longPoll(self):       
        pass

    def query(self):
        self.reportDrivers()

    def discover(self, *args, **kwargs):
        pass

    def delete(self):
        LOGGER.info('Deleting PiCamMonitor Node.')

    def stop(self): # stop the feed and turn off the backlight before stopping the node
        if self.script_running:
            subprocess.call([SPATH + "displaycamera", "killall"])
        elif self.picFrameRunning:
            subprocess.call([SPATH + 'stopPicture'])
        else:
            pass
        
        subprocess.call([SPATH + 'screenoff'])
        self.setDriver('GV1', 0)
        LOGGER.debug('PiCamMonitor stopped.')

    def check_params(self):
        default_script = 0
        default_timer = 20
        default_cam = 'None'
        default_level = 130
        
        if 'screen_connected' in self.polyConfig['customParams']:
            _input = self.polyConfig['customParams']['screen_connected']
            if _input == 'true':
                self.screenConnected = True
        else:
            self.screenConnected = False
        
        if 'start_camera' in self.polyConfig['customParams']:
            self.script = int(self.polyConfig['customParams']['start_camera'])
        else:
            self.script = default_script
 
        if 'pic_frame_enable' in self.polyConfig['customParams']:
            _input = self.polyConfig['customParams']['pic_frame_enable']
            if _input == 'true':
                self.picFrameEnable = True
                self.setDriver('GV6', 1)
        else:
            self.picFrameEnable = False
            self.setDriver('GV6', 0)
               
        if 'pic_frame_auto' in self.polyConfig['customParams']:
            _input = self.polyConfig['customParams']['pic_frame_auto']
            if _input == 'true':
                self.picFrameAuto = True
                self.setDriver('GV12', 1)
        else:
            self.picFrameAuto = False
            self.setDriver('GV12', 0)
        
        if 'cam_screen_level'in self.polyConfig['customParams']:
            self.screenLevel = int(self.polyConfig['customParams']['cam_screen_level'])
        else:
            self.screenLevel = default_level                                          
        self.setDriver('GV5', self.screenLevel)
        
        if 'pic_screen_level' in self.polyConfig['customParams']:
            self.pfscreenLevel = int(self.polyConfig['customParams']['pic_screen_level'])
        else:
            self.pfscreenLevel = default_level
        self.setDriver('GV8', self.pfscreenLevel)
                                           
        if 'cam_screen_timer' in self.polyConfig['customParams']:
            self.cam_screen_timer = int(self.polyConfig['customParams']['cam_screen_timer'])
        else:
            self.cam_screen_timer = default_timer
        self.setDriver('GV4', int(self.cam_screen_timer))                                   
        
        if 'pic_start_folder' in self.polyConfig['customParams']:
            self.pfFolder = int(self.polyConfig['customParams']['pic_start_folder'])
        else:
            self.pfFolder = 0
        self.setDriver('GV11', self.pfFolder)
        
        if 'pic_screen_timer'in self.polyConfig['customParams']:
            self.pic_screen_timer = int(self.polyConfig['customParams']['pic_screen_timer'])
        else:
            self.pic_screen_timer = default_timer
        self.setDriver('GV7', int(self.pic_screen_timer))
        
        if 'sound_on' in self.polyConfig['customParams']:
            _input = self.polyConfig['customParams']['sound_on']
            if _input == 'true':
                self.sound = True
                self.setDriver('GV9', 1)
        else:
            self.sound = False
            self.setDriver('GV9', 0)
            
        #set up the cam feeds and permissions
        
        if 'cam1' in self.polyConfig['customParams']:
            if str.lower(self.polyConfig['customParams']['cam1']) != 'none':
                self.cam1 = self.polyConfig['customParams']['cam1']
                self.cam2x1feed = True
            else:                                                
                self.cam1 = 'none'
        else:
            LOGGER.error('Please enter the cam1 path or none')
           
        if 'cam2' in self.polyConfig['customParams']:
            if str.lower(self.polyConfig['customParams']['cam2']) != 'none':
                self.cam2 = self.polyConfig['customParams']['cam2']
                self.cam2x1feed = True
                self.cam2x2feed = True
            else:                                                
                self.cam2 = 'none'
        else:
            LOGGER.error('Please enter the cam2 path or none')

        if 'cam3' in self.polyConfig['customParams']:
            if str.lower(self.polyConfig['customParams']['cam3']) != 'none':
                self.cam3 = self.polyConfig['customParams']['cam3']
                self.cam2x2feed = True
                self.cam3xfeed = True
            else:                                                
                self.cam3 = 'none'
        else:
            LOGGER.error('Please enter the cam3 path or none')
          
        if 'cam4' in self.polyConfig['customParams']:
            if str.lower(self.polyConfig['customParams']['cam4']) != 'none':
                self.cam4 = self.polyConfig['customParams']['cam4']
                self.cam4xfeed = True
            else:                                                
                self.cam4 = 'none'
        else:
            LOGGER.error('Please enter the cam4 path or none')
            
        if 'triple_feed1' in self.polyConfig['customParams']:
            LOGGER.info('should set feed order')
            if 'triple_feed1' in self.polyConfig['customParams']:
                LOGGER.info('setting feed1')    
                _feed1 = self.polyConfig['customParams']['triple_feed1']
                if _feed1 == 'cam1':
                    self.cam3x_feed1 = self.cam1
                elif _feed1 == 'cam2':
                    self.cam3x_feed1 = self.cam2
                elif _feed1 == 'cam3':
                    self.cam3x_feed1 = self.cam3
                else:
                    pass
                  
            if 'triple_feed2' in self.polyConfig['customParams']:
                LOGGER.info('setting feed2')
                _feed2 = self.polyConfig['customParams']['triple_feed2']
                if _feed2 == 'cam1':
                    self.cam3x_feed2 = self.cam1
                elif _feed2 == 'cam2':
                    self.cam3x_feed2 = self.cam2
                elif _feed2 == 'cam3': 
                    self.cam3x_feed2 = self.cam3
                else:
                    pass
                    
            if 'triple_feed3' in self.polyConfig['customParams']:
                LOGGER.info('setting feed3')
                _feed3 = self.polyConfig['customParams']['triple_feed3']
                if _feed3 == 'cam1':
                    self.cam3x_feed3 = self.cam1
                elif _feed3 == 'cam2':
                    self.cam3x_feed3 = self.cam2
                elif _feed3 == 'cam3': 
                    self.cam3x_feed3 = self.cam3
                else:
                    pass
        else:
            LOGGER.info('just passed the feed order')
            self.cam3x_feed1 = self.cam1
            self.cam3x_feed2 = self.cam2
            self.cam3x_feed3 = self.cam3
    
    def setOn(self, command = None): # fire up the stream(s) and show them for the set time
        if self.screenConnected:
            self.setOff()
            self.runTheFeed = False
        
            if self.script < 4:
                if self.script == 0:
                    feed = self.cam1
                elif self.script == 1:
                    feed = self.cam2
                elif self.script == 2:
                    feed = self.cam3
                elif self.script == 3:
                    feed = self.cam4

                if feed != 'None':
                    self.runTheFeed = True
                    subprocess.call([SPATH + "displaycamera", CAM_SCRIPTS[self.script], feed])
                else:
                    LOGGER.info('No camera feed')
        
            if self.script == 4 and self.cam2x1feed:
                self.runTheFeed = True
                subprocess.call([SPATH + "displaycamera", CAM_SCRIPTS[self.script], self.cam1, self.cam2])
        
            elif self.script == 5 and self.cam2x2feed:
                self.runTheFeed = True
                subprocess.call([SPATH + "displaycamera", CAM_SCRIPTS[self.script], self.cam3, self.cam4])
        
            elif self.script == 6 and self.cam3xfeed:
                self.runTheFeed = True
                subprocess.call([SPATH + "displaycamera", CAM_SCRIPTS[self.script], self.cam3x_feed1, self.cam3x_feed2, self.cam3x_feed3])
       
            elif self.script == 7 and self.cam4xfeed:
                self.runTheFeed = True
                subprocess.call([SPATH + "displaycamera", CAM_SCRIPTS[self.script], self.cam1, self.cam2, self.cam3, self.cam4])
        
        
            if self.runTheFeed:
                LOGGER.info('run the feed')
                self.script_running = True
                subprocess.call([SPATH + "screenBrightness", str(self.screenLevel)])
                time.sleep(2) # allow a bit to get the feeds going
                self.backlight_on()
                self.screenOn_timer2() # the timer thread to turn off the screen
                self.setDriver('GV1', 1)
                self.setDriver('GV2', self.script)
            else:
                self.autoStartPicFrame()
        
        else:
            LOGGER.error('No screen connected')
            return False
            
    def setOff(self, command = None):
        if self.script_running:
            self.backlight_off()
            subprocess.call([SPATH + 'killall'])
            self.setDriver('GV1', 0)
            self.script_running = False
        else:
            return False

    def screenOn_timer2(self): # timer to turn off the screen
        gc.collect()
        t = self.cam_screen_timer
        timer_thread = threading.Timer(t, self.backlight_off)
        timer_thread.daemon = True
        timer_thread.start()
        self.play_sound()
        self.timer_running = True
        #timer_thread.join()
    
    def backlight_off_manual(self, command = None): # from the controller Scrn Off button
        if self.timer_running:
            LOGGER.info('Screen timer running, skipping')
        else:
            subprocess.call([SPATH + 'screenoff'])
            self.setDriver('GV3', 0)
    
    def setScript(self, command = None): # from the drop down list
        LOGGER.info('setting the script')
        if self.picFrameRunning:
            self.backlight_off_manual()
            self.stopPicture()
        else:
            pass
          
        if not self.timer_running:  
            _script = int(command.get('value'))
            if self.script == _script and self.script_running: # check if the script is already running
                self.backlight_on()
                self.screenOn_timer2()
            else:
                LOGGER.debug('changing to another feed')
                self.script = _script
                self.setOn()
        else:
            LOGGER.info('Still running another timer, skipping')
    
    def backlight_on(self, command = None):
        subprocess.call([SPATH + 'screenon'])
        self.setDriver('GV3', 1)
        
    def backlight_off(self, command = None): # called from the screenOn_timer
        subprocess.call([SPATH + 'screenoff'])
        self.setDriver('GV3', 0)
        self.timer_running = False
        self.autoStartPicFrame()
    
    def pictureFrame(self, command = None):
        if self.picFrameEnable and not self.timer_running:
            self.picFrameRunning = True
            pic_thread = threading.Thread(target=self.picFrameStart)
            pic_thread.daemon = True
            pic_thread.start()
            time.sleep(2)
            self.backlight_on()
        else:
            LOGGER.info('Picture Frame not enabled')
    
    def picFrameStart(self):
        subprocess.call([SPATH + "screenBrightness", str(self.pfscreenLevel)])
        subprocess.call([SPATH + "pictureFrame", str(self.pic_screen_timer), PICTURE_FOLDERS[self.pfFolder]])
                                             
    def autoStartPicFrame(self, command = None):
        if self.picFrameEnable and self.picFrameAuto:
            subprocess.call([SPATH + 'killall'])
            self.setDriver('GV1', 0)
            self.script_running = False
            self.pictureFrame()
        else:
            return False
          
    def picFrameAuto(self, command = None):
        _auto = int(command.get('value'))
        self.setDriver('GV12', _auto)
        if _auto == 1:
            self.picFrameAuto = True
            if self.script_running:
                subprocess.call([SPATH + 'killall'])
                self.setDriver('GV1', 0)
                self.script_running = False
            else:
                pass
            self.pictureFrame()
        elif _auto == 0:
            self.picFrameAuto = False
            self.stopPicture()
            
    def stopPicture(self, command = None):
        if self.picFrameRunning:
            subprocess.call([SPATH + 'screenoff'])
            subprocess.call([SPATH + 'stopPicture'])
            self.picFrameRunning = False
        else:
            LOGGER.info('Picture Frame not running')
    
    def soundOn(self, command):
        _sound = int(command.get('value'))
        if _sound == 1:
            self.sound = True
            self.setDriver('GV9', 1)
            self.play_sound()  
        else:
            self.sound = False
            self.setDriver('GV9', 0)
    
    def play_sound(self):
        if self.sound:
            subprocess.call([SPATH + '2tone'])
        else:
            return False
    
    def setScreenOnTime(self, command = None):
        self.cam_screen_timer = int(command.get('value'))
        self.setDriver('GV4', self.cam_screen_timer)
    
    def setScreenLevel(self, command = None):
        self.screenLevel = int(command.get('value'))
        self.setDriver('GV5', self.screenLevel)
        subprocess.call([SPATH + "screenBrightness", str(self.screenLevel)])
    
    def picFrameFolder(self, command = None):
        _folder = int(command.get('value'))
        self.setDriver('GV11', _folder)
        self.pfFolder = _folder
        if self.picFrameAuto:
            self.stopPicture()
            self.pictureFrame()
        else:
            pass
      
    def setPFscreenLevel(self, command = None):
        _level = int(command.get('value'))
        self.pfscreenLevel = _level
        self.setDriver('GV8', _level)
        subprocess.call([SPATH + "screenBrightness", str(self.pfscreenLevel)])
    
    def setPFscreenOnTime(self, command = None):
        _time = int(command.get('value'))
        self.setDriver('GV7', _time)
        self.pic_screen_timer = _time
        self.stopPicture()
        self.pictureFrame()
    
    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all:')
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    drivers = [{'driver': 'ST', 'value': 1, 'uom': 2},    #online
               {'driver': 'GV1', 'value': 0, 'uom': 2},   #feed playing
               {'driver': 'GV2', 'value': 0, 'uom': 25},  #feed name
               {'driver': 'GV3', 'value': 0, 'uom': 2},   #screen on
               {'driver': 'GV4', 'value': 0, 'uom': 56},  #cam timer
               {'driver': 'GV5', 'value': 0, 'uom': 56},  #cam bright
               {'driver': 'GV6', 'value': 0, 'uom': 2},   #pf enabled
               {'driver': 'GV7', 'value': 0, 'uom': 56},  #pf timer
               {'driver': 'GV8', 'value': 0, 'uom': 56},  #pf bright
               {'driver': 'GV9', 'value': 0, 'uom': 2},  #sound
               {'driver': 'GV12', 'value': 0, 'uom': 2},  #pf auto
               {'driver': 'GV11', 'value': 0, 'uom':25}   #pf folder
              ]
            
    id = 'controller'
    commands = {
                'DON': setOn,
                'DOF': setOff,
                'BACKLIGHT_ON':backlight_on,
                'BACKLIGHT_OFF':backlight_off_manual,   
                'PICFRAME_ON': pictureFrame,
                'PICFRAME_OFF': stopPicture,
                'QUERY': query,
                'UPDATE_PROFILE': update_profile,
                'CAMERA': setScript,
                'SCREENONTIME': setScreenOnTime,
                'SCREENBRIGHTNESS': setScreenLevel,
                'PIC_FRAME_AUTO': picFrameAuto,
                'FOLDER': picFrameFolder,
                'PFSCREENBRIGHTNESS': setPFscreenLevel,
                'PFSCREENONTIME': setPFscreenOnTime,
                'SOUND_ON': soundOn
               }

    
if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('PiCamMonitor')
        """
        Instantiates the Interface to Polyglot.
        """
        polyglot.start()
        """
        Starts MQTT and connects to Polyglot.
        """
        control = Controller(polyglot)
        """
        Creates the Controller Node and passes in the Interface
        """
        control.runForever()
        """
        Sits around and does nothing forever, keeping your program running.
        """
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
        """
        Catch SIGTERM or Control-C and exit cleanly.
        """

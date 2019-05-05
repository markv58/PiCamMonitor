#!/usr/bin/env python3
"""
PiCamMonitor v2.0.1
This is a NodeServer for UDI Polyglot v2 that will display your ip camera sub-feeds on a 
Raspberry Pi 3 B+ with attached official 7" touch screen.
When not showing a camera feed an optional picture frame mode can display images from different folders.
An option for MagicMirror control has been added.
An option to control clones has been added.
CloneCtrl1a is the required version for clone control.
"""
import polyinterface
import sys
import time
import os
import json
import subprocess
import threading
import requests

LOGGER = polyinterface.LOGGER
SPATH = "/home/pi/.polyglot/nodeservers/PiCamMonitor/Scripts/./"
XSPATH = "/home/pi/.polyglot/nodeservers/PiCamMonitor/Scripts/./screenCtrl.sh"

# list of args to pass to displaycamera - Do Not Alter
CAM_SCRIPTS = ['camera1', #1
               'camera1', #2
               'camera1', #3
               'camera1', #4
               'cams2x1', #5
               'cams2x2', #6
               'cams3x',  #7
               'cams4x'   #8
              ]

CLN_SCRIPTS = ['camera1', #1
               'camera2', #2
               'camera3', #3
               'camera4', #4
               'cams2x1', #5
               'cams2x2', #6
               'cams3x',  #7
               'cams4x'   #8
              ]

# list of args to pass to pictureFrame - Do Not Alter
PICTURE_FOLDERS = ['/home/pi/Pictures/Family',       #1
                   '/home/pi/Pictures/Friends',      #2
                   '/home/pi/Pictures/Kids',         #3
                   '/home/pi/Pictures/Vacation',     #4
                   '/home/pi/Pictures/Christmas',    #5
                   '/home/pi/Pictures/Valentines',   #6
                   '/home/pi/Pictures/StPatricks',   #7
                   '/home/pi/Pictures/Easter',       #8
                   '/home/pi/Pictures/YomKippur',    #9
                   '/home/pi/Pictures/Halloween',    #10
                   '/home/pi/Pictures/Thanksgiving', #11
                   '/home/pi/Pictures/NewYears',     #12
                   '/home/pi/Pictures/Birthday1',    #13
                   '/home/pi/Pictures/Birthday2',    #14
                   '/home/pi/Pictures/Birthday3',    #15
                   '/home/pi/Pictures/Birthday4',    #16
                   '/home/pi/Pictures/Birthday5',    #17
                   '/home/pi/Pictures/User1',        #18
                   '/home/pi/Pictures/User2',        #19
                   '/home/pi/Pictures/User3',        #20
                   '/home/pi/Pictures/User4'         #21
                  ]

class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super(Controller,self).__init__(polyglot)
        self.name = 'PiCamMonitor'
        self.script = 0
        self.script_running = False    #setting all of the variables to their initial state
        self.timer_running = False
        self.picFrameRunning = False
        self.MMinstalled = False
        self.MMrunning = False
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
        self.picFrameAuto = 0   
        self.picFrameEnable = False        
        self.pfscreenLevel = 50
        self.pic_screen_timer = 20
        #self.screenConnected = False
        self.sound = False
        self.pfFolder = 0
        self.cam3x_feed1 = self.cam1
        self.cam3x_feed2 = self.cam2
        self.cam3x_feed3 = self.cam3
        self.clones = False
        self.ignoreSync = False
        self.clonesInSync = True
        self.standalone = False
        
    def start(self):
        self.removeNoticesAll()
        LOGGER.info('Started PiCamMonitor')
        time.sleep(1)
        LOGGER.info('Checking custom parameters')
        self.check_params() #override the initial variables with custom parameters
        time.sleep(1)        
        self.settheflags()
        time.sleep(1)
        self.backlight_off_manual()
        LOGGER.info('Checking the status of any clones and starting Feature if enabled')
        time.sleep(2)
        self.cloneSync()
        time.sleep(2)
        self.query()
        LOGGER.info('Start up is complete')
        LOGGER.info('CloneCtrl1a is required on each clone for control')
          
    def shortPoll(self):
        if self.script_running and self.picFrameAuto > 0: # Skip the short poll while a camera feed is displayed
            pass                                          # and a feature is enabled
        else:
            self.clonesInSync = True
            for node in self.nodes:
                self.nodes[node].update()
                _sync = self.nodes[node].getSync()
                _online = self.nodes[node].getOnline()
                if not _sync and _online:
                    self.clonesInSync = False
                else:
                    pass
            if not self.clonesInSync:
                self.autoCloneSync()   
            else:
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
        self.setDriver('ST', 0)
        self.setDriver('GV1', 0)
        self.sendSelfCmd('killall')
        self.sendSelfCmd('off')
        self.sendCloneCmd('killall')
        self.sendCloneCmd('off')
        LOGGER.info('PiCamMonitor stopped.')
        
    def check_params(self):
        default_script = 0
        default_timer = 60
        default_cam = 'none'
        cam_default_level = 130
        pf_default_level = 50
        
        _params = self.polyConfig['customParams']
        for key, val in _params.items():    
            _key = key.lower()
            if _key.startswith('clone'):
                self.clones = True
                _address = val
                nodeAddress = _address.replace('.','')
                self.addNode(CloneNode(self, self.address, nodeAddress, _address, 'PCM-' + key))
            else:
                pass
 
        if 'stand_alone' in self.polyConfig['customParams']:
            _input = self.polyConfig['customParams']['stand_alone']
            if _input == 'true':
                self.standalone = True
                LOGGER.info('Running in Stand Alone mode')
            elif _input == 'false' or not self.standalone:
                LOGGER.info('Running in Controller mode')
                
        if 'mm_installed' in self.polyConfig['customParams']:
            _input = self.polyConfig['customParams']['mm_installed']
            if _input == 'true':
                self.MMinstalled = True
                self.setDriver('GV6', 1)
        else:
            self.MMinstalled = False
            self.setDriver('GV6', 0)
               
        if 'feature_auto_start' in self.polyConfig['customParams']:
            _input = int(self.polyConfig['customParams']['feature_auto_start'])
            if _input == 0:
                self.picFrameAuto = 0
                self.setDriver('GV12', 0)
            elif _input == 1:
                self.picFrameAuto = 1
                self.setDriver('GV12', 1)
            elif _input == 2:
                self.picFrameAuto = 2
                self.setDriver('GV12', 2)
        else:
            self.picFrameAuto = 0
            self.setDriver('GV12', 0)
        
        if 'cam_screen_level'in self.polyConfig['customParams']:
            _level = int(self.polyConfig['customParams']['cam_screen_level'])
            if _level > -1 and _level < 251:
                self.screenLevel = _level
            else:
                self.screenLevel = cam_default_level                                          
        self.setDriver('GV5', self.screenLevel)
        
        if 'feature_screen_level' in self.polyConfig['customParams']:
            _level = int(self.polyConfig['customParams']['feature_screen_level'])
            if _level > -1 and _level < 251:
                self.pfscreenLevel = _level
            else:
                self.pfscreenLevel = pf_default_level
        self.setDriver('GV8', self.pfscreenLevel)                                 
        
        if 'cam_screen_timer' in self.polyConfig['customParams']:
            _level = int(self.polyConfig['customParams']['cam_screen_timer'])
            if _level > 9 and _level < 121:
                self.cam_screen_timer = _level
            else:
                self.cam_screen_timer = default_timer
        self.setDriver('GV4', int(self.cam_screen_timer))                                   
        
        if 'pic_frame_folder' in self.polyConfig['customParams']:
            _folder = int(self.polyConfig['customParams']['pic_frame_folder'])
            _folder -= 1
            if _folder > -1 and _folder < 21:
                self.pfFolder = _folder
            else:
                self.pfFolder = 0
        self.setDriver('GV11', self.pfFolder)
        
        if 'pic_frame_timer'in self.polyConfig['customParams']:
            _level = int(self.polyConfig['customParams']['pic_frame_timer'])
            if _level > 9 and _level < 121:
                self.pic_screen_timer = _level
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
                self.cam2x2feed = False
        else:
            LOGGER.error('Please enter the cam4 path or none')
        
        if 'triple_feed1' in self.polyConfig['customParams']:
            #LOGGER.info('should set feed order')
            if 'triple_feed1' in self.polyConfig['customParams']:
                #LOGGER.info('setting feed1')    
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
                #LOGGER.info('setting feed2')
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
                #LOGGER.info('setting feed3')
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
            self.cam3x_feed1 = self.cam1
            self.cam3x_feed2 = self.cam2
            self.cam3x_feed3 = self.cam3

        if 'pic_frame_enable' in self.polyConfig['customParams']:
            self.addNotice('Please delete pic_frame_enable from the custom parameters')
        
        if 'pic_frame_level' in self.polyConfig['customParams']:
            self.addNotice('Please delete pic_frame_level from the custom parameters')
            
        if 'pic_frame_auto' in self.polyConfig['customParams']:
            self.addNotice('Please delete pic_frame_auto from the custom parameters')
        
        if 'screen_connected' in self.polyConfig['customParams']:
            self.addNotice('Please delete screen_connected from the custom parameters. If you have updated from v1 please hit the Update Profile button and re-start the admin console.')
            
        if 'start_camera' in self.polyConfig['customParams']:
            self.addNotice('Please delete start_camera from the custom parameters')
            
        
    ####----------- Start of the fun confusing stuff ----------------------------
   
    def setOn(self, command = None): # fire up the stream(s) and show them for the set time
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
            if feed != 'none':
                self.runTheFeed = True
                self.sendSelfCmd(CAM_SCRIPTS[self.script], feed)
                self.sendCloneCmd(CLN_SCRIPTS[self.script])
            else:
                LOGGER.error('No camera is listed in Configuration')
        if self.script == 4 and self.cam2x1feed:
            self.runTheFeed = True
            self.sendSelfCmd(CAM_SCRIPTS[self.script], self.cam1, self.cam2)
            self.sendCloneCmd(CLN_SCRIPTS[self.script])
        elif self.script == 5 and self.cam2x2feed:
            self.runTheFeed = True
            self.sendSelfCmd(CAM_SCRIPTS[self.script], self.cam3, self.cam4)
            self.sendCloneCmd(CLN_SCRIPTS[self.script])
        elif self.script == 6 and self.cam3xfeed:
            self.runTheFeed = True
            self.sendSelfCmd(CAM_SCRIPTS[self.script], self.cam3x_feed1, self.cam3x_feed2, self.cam3x_feed3)
            self.sendCloneCmd(CLN_SCRIPTS[self.script])
        elif self.script == 7 and self.cam4xfeed:
            self.runTheFeed = True
            self.sendSelfCmd(CAM_SCRIPTS[self.script], self.cam1, self.cam2, self.cam3, self.cam4)
            self.sendCloneCmd(CLN_SCRIPTS[self.script])
        if self.runTheFeed:
            LOGGER.info('run the feed for %s', CLN_SCRIPTS[self.script])
            self.setDriver('GV1', 1)
            self.setDriver('GV2', self.script)              
            self.script_running = True
            self.sendSelfCmd(str(self.screenLevel))
            self.sendCloneCmd(str(self.screenLevel))
            time.sleep(2) # allow a bit to get the feeds going
            self.backlight_on()
            self.screenOn_timer2() # the timer thread to turn off the screen
        else:
            self.autoStartPicFrame()
            
    def setOff(self, command = None):
        if self.script_running:
            self.stopCamFeed()
        else:
            return False

    def screenOn_timer2(self): # timer to turn off the screen
        t = self.cam_screen_timer
        timer_thread = threading.Timer(t, self.backlight_off)
        timer_thread.daemon = True
        timer_thread.start()
        self.play_sound()
        self.timer_running = True

    def setScript(self, command = None): # from the drop down list
        if self.picFrameRunning or self.MMrunning: #turn off the screen for transition to cam feed
            self.backlight_off_manual()
        else:
            pass
        if not self.timer_running:  
            _script = int(command.get('value'))
            if self.script == _script and self.script_running: # check if the cam script is already running
                self.backlight_on()
                self.screenOn_timer2()
            else:                                              #switch to the new script
                self.script = _script
                self.setOn()
        else:
            LOGGER.info('Still running another timer, skipping')
    
    def backlight_on(self, command = None):
        self.sendSelfCmd('on')
        self.sendCloneCmd('on')
        self.setDriver('GV3', 1)
        
    def backlight_off(self, command = None): # called from the screenOn_timer
        self.timer_running = False
        self.sendSelfCmd('off')
        self.sendCloneCmd('off')
        self.setDriver('GV3', 0)
        self.autoStartPicFrame() #go see if a Feature is selected and installed or enabled
    
    def backlight_off_manual(self, command = None): # from the controller Screen Off button, toggles the backlight off
        if self.timer_running:
            LOGGER.info('Screen timer running, skipping')
        else:
            self.sendSelfCmd('off')
            self.sendCloneCmd('off')
            self.setDriver('GV3', 0)    
    
    def picFrameStart(self): # called from Picture Frame
        _time = str(self.pic_screen_timer)
        _folder = PICTURE_FOLDERS[self.pfFolder]
        self.sendSelfCmd(str(self.pfscreenLevel))
        self.sendSelfCmd('pictureFrame', _time, _folder)  
       
    def pictureFrame(self):
        self.picFrameRunning = True
        LOGGER.info('Starting PictureFrame')
        pic_thread = threading.Thread(target=self.picFrameStart)
        pic_thread.daemon = True
        pic_thread.start()
        time.sleep(2)
        self.backlight_on()
        self.picFrameClones()
        
    def picFrameClones(self):
        _level = str(self.pfscreenLevel) # for the clones
        self.sendCloneCmd(_level)       
        self.sendCloneCmd('pf' + str(self.pfFolder))
    
    def autoStartPicFrame(self, command = None):
        if self.picFrameAuto == 1 and not self.picFrameRunning:
            self.stopCamFeed()
            self.pictureFrame()
        elif self.picFrameAuto == 1 and self.picFrameRunning:   
            self.stopCamFeed()
            self.backlight_on()
        elif self.picFrameAuto == 2 and self.MMinstalled  and not self.MMrunning:
            self.stopCamFeed()
            self.startMM()
        elif self.picFrameAuto == 2 and self.MMinstalled  and self.MMrunning:
            self.stopCamFeed()
            self.sendSelfCmd(str(self.pfscreenLevel))
            self.sendCloneCmd(str(self.pfscreenLevel))
            self.backlight_on() 
        elif self.picFrameAuto == 0:
            pass
    
    def picFrameAuto(self, command = None): # triggered by the Optional Feature drop down
        _auto = int(command.get('value'))
        if _auto == 0: # stop any running Feature
            self.picFrameAuto = 0
            self.setDriver('GV12', 0)
            if self.timer_running:
                self.stopFeatureLive()
            else:    
                self.stopFeature()
 
        elif _auto == 1: #run Picture Frame
            self.picFrameAuto = 1
            self.setDriver('GV12', 1)
            if self.script_running and not self.timer_running: #stop the cam feed
                self.stopCamFeed()
                self.pictureFrame()
            elif self.script_running and self.timer_running:
                self.stopFeatureLive()
            else:
                self.stopFeature()
                self.pictureFrame()
                
        elif _auto == 2: # run MagicMirror
            if self.MMinstalled:
                self.picFrameAuto = 2
                self.setDriver('GV12', 2)
                if self.script_running and not self.timer_running:    #stop the cam feed first
                    self.stopCamFeed()
                    self.startMM()
                elif self.script_running and self.timer_running:
                    self.stopFeatureLive()
                else:    
                    self.stopFeature()
                    self.startMM()
            else:
                LOGGER.info('MagicMirror is not installed')
    
    def stopCamFeed(self, command = None):
        self.sendSelfCmd('off')
        self.sendCloneCmd('off')
        self.sendSelfCmd('omxkill')
        self.sendCloneCmd('omxkill')
        self.setDriver('GV1', 0)
        self.script_running = False
          
    def startMM(self, command = None):
        LOGGER.info('Starting MagicMirror')
        self.sendSelfCmd('MMstart')
        self.sendCloneCmd('MMstart')
        time.sleep(6)             #let MM get started before turning on the backlight
        self.sendSelfCmd(str(self.pfscreenLevel))
        self.sendSelfCmd('on')
        self.sendCloneCmd(str(self.pfscreenLevel))
        self.sendCloneCmd('on')
        self.MMrunning = True
        
    def stopFeature(self):
        self.sendSelfCmd('off')
        if self.picFrameRunning:
            self.sendSelfCmd('pkill')
        elif self.MMrunning:
            self.sendSelfCmd('mkill')
        self.sendCloneCmd('off')
        self.sendCloneCmd('pkill')
        self.MMrunning = False
        self.picFrameRunning = False
 
    def stopFeatureLive(self):
        if self.picFrameRunning:
            self.sendSelfCmd('pkill')
        elif self.MMrunning:
            self.sendSelfCmd('mkill')
        self.sendCloneCmd('pkill')
        self.MMrunning = False
        self.picFrameRunning = False

    def soundOn(self, command):
        _sound = int(command.get('value'))
        if _sound == 1:
            self.sound = True
            self.setDriver('GV9', 1)
            self.play_sound()  
        else:
            self.sound = False
            self.setDriver('GV9', 0)
    
    def play_sound(self):      #work on this one
        if self.sound and self.standalone:
            self.sendCloneCmd('playsound')
            subprocess.call([SPATH + '2tone'])
        elif self.sound:
            self.sendCloneCmd('playsound')
        else:
            return False
    
    def setScreenOnTime(self, command = None):
        self.cam_screen_timer = int(command.get('value'))
        self.setDriver('GV4', self.cam_screen_timer)
    
    def setScreenLevel(self, command = None): # sets cam feed level
        self.screenLevel = int(command.get('value'))
        self.setDriver('GV5', self.screenLevel)
        if self.timer_running:
            self.sendSelfCmd(str(self.screenLevel))
            self.sendCloneCmd(str(self.screenLevel))
        else:
            pass
        
    def picFrameFolder(self, command = None):
        _folder = int(command.get('value'))
        self.setDriver('GV11', _folder)
        self.pfFolder = _folder
        if self.picFrameAuto == 1 and self.picFrameRunning:
            self.stopFeature()
            self.pictureFrame()
        else:
            pass
      
    def setPFscreenLevel(self, command = None): # sets feature level
        _level = int(command.get('value'))
        self.pfscreenLevel = _level
        self.setDriver('GV8', _level)
        if not self.timer_running:
            self.sendSelfCmd(str(self.pfscreenLevel))
            self.sendCloneCmd(str(self.pfscreenLevel))
        else:
            pass
          
    def sendSelfCmd(self, *args):
        if self.standalone:
            subprocess.call([XSPATH, *args])
        else:
            pass

    def sendCloneCmd(self, command):
        if self.clones:
            for node in self.nodes:
                ip = self.nodes[node].getip()
                if self.ignoreSync:
                    _sync = True
                else:
                    _sync = self.nodes[node].getSync()
                    
                if ip != None and _sync:
                    try:
                        url = 'http://' + ip + ':6502/cgi-bin/CloneCtrl1a?' + command
                        r = requests.get(url, verify=False, timeout=2)                
                    except requests.exceptions.Timeout:
                        self.nodes[node].setSyncFalse()
                        self.cloneSyncBad = True
                        LOGGER.warning('There was a problem sending the command to clone %s', ip)
                        return None
                else:
                    pass
        else:
            return False
      
    def shutDownPi(self,command):
        LOGGER.info('Shutting down the Clones and Stand Alone Master')
        self.setDriver('ST', 0)
        self.sendCloneCmd('shutDownPi')
        time.sleep(10)
        self.sendSelfCmd('shutDownPi')
    
    def piReboot(self,command):
        LOGGER.info('Rebooting all Clones now and the Stand Alone Master in 10 seconds')
        self.setDriver('ST', 0) 
        self.sendCloneCmd('rebootPi')
        time.sleep(10)
        self.sendSelfCmd('rebootPi')
    
    def autoCloneSync(self):
        if self.clones:
            LOGGER.warning('A clone is out of sync, Synchronizing in 20 seconds.')
            time.sleep(20)
            self.cloneSync()   
        else:
            pass
          
    def cloneSync(self, command = None):
        while self.timer_running:
            time.sleep(1)
        LOGGER.info('Synchronizing the Controller and Clones')
        self.ignoreSync = True
        time.sleep(2)
        self.sendSelfCmd('killall')
        self.sendCloneCmd('killall')
        for node in self.nodes:
            self.nodes[node].setSyncTrue() 
        self.picFrameRunning = False
        self.MMrunning = False
        self.ignoreSync = False
        self.clonesInSync = True
        self.shortPoll()
        self.autoStartPicFrame()
        
    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all:')
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st
    
    def settheflags(self):
        if self.standalone:
            subprocess.call('sudo chmod -R +x /home/pi/.polyglot/nodeservers/PiCamMonitor/Scripts/', shell=True)
            subprocess.call([SPATH + 'setupfolders.sh', 'normal'])
            subprocess.call([SPATH + 'setupMM.sh', 'normal'])
        else:
            pass
          
    #### --- Necessary files - Do Not Delete --- ####
      
    def update(self):
        pass    
    
    def setSyncTrue(self):
        pass
    
    def CloneCmd(self):
        pass
    
    def getip(self):
        pass
    
    def getSync(self):
        return True
    
    def getOnline(self):
        return True
      
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
               {'driver': 'GV12', 'value': 0, 'uom': 25},  #pf auto
               {'driver': 'GV11', 'value': 0, 'uom':25}   #pf folder
              ]
            
    id = 'controller'
    commands = {
                'BACKLIGHT_ON':backlight_on,
                'BACKLIGHT_OFF':backlight_off_manual,   
                'QUERY': query,
                'UPDATE_PROFILE': update_profile,
                'SYNC_CLONES': cloneSync,
                'SHUT_DOWN': shutDownPi,
                'REBOOT_PI': piReboot,
                'REMOVE_NOTICES_ALL': remove_notices_all,
                'CAMERA': setScript,
                'SCREENONTIME': setScreenOnTime,
                'SCREENBRIGHTNESS': setScreenLevel,
                'PIC_FRAME_AUTO': picFrameAuto,
                'FOLDER': picFrameFolder,
                'PFSCREENBRIGHTNESS': setPFscreenLevel,
                'SOUND_ON': soundOn
               }

class PingHelper(object):

    def __init__(self, ip, timeout):
        self.ip = ip
        self.timeout = timeout

    def ping(self):
        try:
            response = os.system("ping -c 1 -W " + str(self.timeout) + " " + self.ip)
            if response == 0:
                return response
            else:
                return None
        except:
            # Capture any exception
            return None
 
class CloneNode(polyinterface.Node):
    def __init__(self, controller, primary, address, ipaddress, name):
        super(CloneNode, self).__init__(controller, primary, address, name)
        self.ip = ipaddress
        self.scan = 1
        self.strength = 0
        self.cloneSync = False
        self.online = False
        
    def start(self):
        self.update    

    def setOn(self):
        self.setDriver('ST', 1)
        self.online = True

    def setOff(self):
        self.setDriver('ST', 0)
        self.online = False

    def update(self):
        if (self.scan):
            onnet = PingHelper(ip=self.ip,timeout=1)
            result = onnet.ping()
            if (result != None):
                self.setOnNetwork(5)
                #LOGGER.debug('Network ' + self.ip + ': OK')
            elif (self.strength > 1):
                self.setOnNetwork(self.strength - 1)
                self.cloneSync = False
                LOGGER.info('Network ' + self.ip + ': In Fault')
            elif (self.strength == 1):
                LOGGER.info('Network ' + self.ip + ': Out of Network')
                self.setOffNetwork()             
            
    def setOnNetwork(self,strength):
        self.setOn()
    
    def setOffNetwork(self):
        self.setDriver('GV0', 0)
        self.cloneSync = False
    
    def query(self):
        self.reportDrivers()     
    
    def setSyncTrue(self):
        self.cloneSync = True
        self.setDriver('GV0', 1)
    
    def setSyncFalse(self):
        self.cloneSync = False
        self.setDriver('GV0', 0)
        
    def getip(self):
        ip = self.ip
        return ip
    
    def getSync(self):
        sync = self.cloneSync
        return sync  
    
    def getOnline(self):
        _online = self.online
        return _online
    
    def CloneCmd(self,command):
        _ip = str(self.ip)
        url = 'http://' + _ip + ':6502/cgi-bin/CloneCtrl1a?' + command
        requests.get(url)

    def getSync(self):
        sync = self.cloneSync
        return sync
    
    def shutDownPi(self,command):
        LOGGER.info('Shutting down the Clone')
        self.cloneSync = False
        self.setOff()
        self.setDriver('GV0', 0)
        time.sleep(2)
        self.CloneCmd('off')
        self.CloneCmd('shutDownPi')
    
    def piReboot(self,command):
        LOGGER.info('Rebooting the Clone in 2 seconds')
        self.cloneSync = False
        self.setOff()
        self.setDriver('GV0', 0)
        time.sleep(2)
        self.CloneCmd('off')
        time.sleep(1)
        self.CloneCmd('rebootPi')

    drivers = [
               {'driver': 'ST', 'value': 0, 'uom': 2},
               {'driver': 'GV0', 'value': 0, 'uom': 2}
              ]

    id = 'clone'

    commands = {
                'SHUT_DOWN': shutDownPi,
                'REBOOT_PI': piReboot
               }

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('PiCamMonitor')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)

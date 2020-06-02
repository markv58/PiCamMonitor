#!/usr/bin/env python3
"""
PiCamMonitor v2.3.0rc2
This is a NodeSever for UDI Polyglot v2 that will display your ip camera sub-feeds on a
Raspberry Pi 3 B+ with attached official 7" touch screen or any other monitor or tv screen with a couple of limitations.
When not showing a camera feed an optional picture frame mode can display images from different folders.
An option for MagicMirror control has been added.
An option to control clones has been added.
A camera hold feature has been added.
CloneCtrl3 is the required version for clone control.
"""
import polyinterface
import sys
import time
import os
import json
import subprocess
import threading
import requests
import logging
from subprocess import DEVNULL, STDOUT, check_call

LOGGER = polyinterface.LOGGER
logging.getLogger('urllib3').setLevel(logging.ERROR)


SPATH = "/home/pi/.polyglot/nodeservers/PiCamMonitor/Scripts/./"

XSPATHGEN = "/home/pi/.polyglot/nodeservers/PiCamMonitor/Scripts/./screenCtrlGen.sh"
XSPATH = "/home/pi/.polyglot/nodeservers/PiCamMonitor/Scripts/./screenCtrl.sh"

SOUNDPATH = "/Sounds/"

# list of args to pass to displaycamera - Do Not Alter
CAM_SCRIPTS = ['camera1', #1
               'camera1', #2
               'camera1', #3
               'camera1', #4
               'camera1', #5
               'camera1', #6
               'camera1', #7
               'camera1', #8
               'camera1', #9
               'camera1', #10
               'camera1', #11
               'camera1', #12
               'camera1', #13
               'camera1', #14
               'camera1', #15
               'camera1', #16
               'camera1', #17
               'camera1', #18
               'camera1', #19
               'camera1', #20
               'camera1', #21
               'camera1', #22
               'camera1', #23
               'camera1', #24
               'camera1', #25
               'camera1', #26 BI Group 1
               'camera1', #27 BI Group 2
               'camera1', #28 BI Group 3
               'camera1', #29 BI Group 4
               'camera1', #30 BI Group 5
               'cams2x1', #31
               'cams2x2', #32
               'cams3x',  #33
               'cams4x'   #34
              ]

CLN_SCRIPTS = ['camera1', #1
               'camera2', #2
               'camera3', #3
               'camera4', #4
               'camera5', #5
               'camera6', #6
               'camera7', #7
               'camera8', #8
               'camera9', #9
               'camera10', #10
               'camera11', #11
               'camera12', #12
               'camera13', #13
               'camera14', #14
               'camera15', #15
               'camera16', #16
               'camera17', #17
               'camera18', #18
               'camera19', #19
               'camera20', #20
               'camera21', #21
               'camera22', #22
               'camera23', #23
               'camera24', #24
               'camera25', #25
               'camera26', #26 BI
               'camera27', #27 BI
               'camera28', #28 BI
               'camera29', #29 BI
               'camera30', #30 BI
               'cams2x1',  #31
               'cams2x2',  #32
               'cams3x',   #33
               'cams4x'    #34
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

SOUNDS = ['sound0',      # 0 off
          'sound1',      # 1 piezo
          'sound2.wav',  # 2 doorbell
          'sound3.wav',  # 3 dog bark
          'sound4.wav',  # 4 car honk
          'sound5.wav',  # 5 splash
          'sound6.wav',  # 6 police siren
          'sound7.wav',  # 7 baby sneeze
          'sound8.wav',  # 8 chime
          'sound9.wav',  # 9 bell
          'sound10.wav', # 10 ships bell
          'sound11.wav',  # 11 error
          'sound12.wav',  # 12 buzzer
          'sound13.wav',  # 13 smoke alarm
          'sound14.wav',  # 14 custon1
          'sound15.wav',  # 15 custon2
          'sound16.wav',  # 16 custon3
          'sound17.wav',  # 17 custon4
         ]


GC_LIST = ['on', 'of','ca', 'pf', 'pk', 'om', 'ki', 'sh', 're', 'MM', 'un', 'pl', 'so', 'mk', 'pi', 'sh', 're', 'sb']   # A list for devices with generic screens to parse out non Official RPi screen commands


class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super(Controller,self).__init__(polyglot)
        self.name = 'PiCamMonitor'
        self.script = 0
        self.static = False
        self.script_running = False    #setting all of the variables to their initial state
        self.timer_running = False
        self.picFrameRunning = False
        self.MMinstalled = False
        self.MMrunning = False
        self.runTheFeed = True
        self.camFeed = False
        self.cam2x1feed = False
        self.cam2x2feed = False
        self.cam3xfeed = False
        self.cam4xfeed = False
        self.cam1 = 'none'
        self.cam2 = 'none'
        self.cam3 = 'none'
        self.cam4 = 'none'
        self.cam5 = 'none'
        self.cam6 = 'none'
        self.cam7 = 'none'
        self.cam8 = 'none'
        self.cam9 = 'none'
        self.cam10 = 'none'
        self.cam11 = 'none'
        self.cam12 = 'none'
        self.cam13 = 'none'
        self.cam14 = 'none'
        self.cam15 = 'none'
        self.cam16 = 'none'
        self.cam17 = 'none'
        self.cam18 = 'none'
        self.cam19 = 'none'
        self.cam20 = 'none'
        self.cam21 = 'none'
        self.cam22 = 'none'
        self.cam23 = 'none'
        self.cam24 = 'none'
        self.cam25 = 'none'
        self.cam26 = 'none'
        self.cam27 = 'none'
        self.cam28 = 'none'
        self.cam29 = 'none'
        self.cam30 = 'none'
        self.screenLevel = 130
        self.cam_screen_timer = 20
        self.picFrameAuto = 0
        self.picFrameEnable = False
        self.pfscreenLevel = 50
        self.pic_screen_timer = 60
        self.genScreenConnected = False
        self.sound = 0
        self.playSound = False
        self.pfFolder = 0
        self.cam3x_feed1 = self.cam1
        self.cam3x_feed2 = self.cam2
        self.cam3x_feed3 = self.cam3
        self.clones = False
        self.ignoreSync = False
        self.clonesInSync = True
        self.standalone = False
        self.genMasterSB = False
        self.show_debug_log = False
        self.show_info_log = False
        self.screen_on = True

    def start(self):
        self.removeNoticesAll()
        LOGGER.info('Started PiCamMonitor')
        time.sleep(1)
        self.set_logging(10)
        LOGGER.info('Checking custom parameters')
        self.check_params() #override the initial variables with custom parameters
        time.sleep(1)
        self.settheflags()
        time.sleep(1)
        LOGGER.info('Checking the status of any clones and starting Feature if enabled')
        time.sleep(1)
        self.cloneSync()
        time.sleep(2)
        self.query()
        if self.sound > 0: self.play_sound(self.sound)
        LOGGER.info('Start up is complete, version 2.3.0rc2')
        LOGGER.info('CloneCtrl3 is required on each clone for control')
        LOGGER.info('If your clones are not resopnding please update them')
        LOGGER.info('Instructions for updating clones are here: https://github.com/markv58/PCM-UDI-Clone')

    def shortPoll(self):
        pass

        #if self.script_running: # Skip the short poll while a camera feed is displayed
        #    pass
        #else:
        #    self.clonesInSync = True
        #    for node in self.nodes:
        #        self.nodes[node].update()
        #        _sync = self.nodes[node].getSync()
        #        _online = self.nodes[node].getOnline()
        #        if not _sync and _online:
        #            self.clonesInSync = False
        #        else:
        #            pass
        #    if not self.clonesInSync:
        #        self.autoCloneSync()
        #    else:
        #        pass

    def longPoll(self):
        pass

    def query(self):
        self.reportDrivers()

    def discover(self, *args, **kwargs):
        pass

    def delete(self):
        LOGGER.info('Deleting PiCamMonitor Node.')

    def stop(self): # stop the feed and turn off the backlight before stopping the node
        self.sendSelfCmd('killall')
        self.sendCloneCmd('killall')
        #if not self.genScreenConnected: self.sendSelfCmd('off')
        self.setDriver('ST', 0)
        self.setDriver('GV1', 0)
        for node in self.nodes:
            self.nodes[node].setOffNetwork()
        LOGGER.info('PiCamMonitor stopped.')

    def check_params(self):
        default_script = 0
        default_timer = 60
        default_cam = 'none'
        cam_default_level = 130
        pf_default_level = 50
        self.sound = 0
        self.pic_frame_folder = 0

        _params = self.polyConfig['customParams']   # Send in the Clones
        for key, val in _params.items():
            _key = key.lower()
            if _key.startswith('clone') or _key.startswith('gen_clone'):
                self.clones = True
                _address = val
                nodeAddress = _address.replace('.','')
                self.addNode(CloneNode(self, self.address, nodeAddress, _address, 'PCM-' + key))
            elif _key == 'start_in_debug':
               if val.lower() == 'yes' or val.lower() == 'true':
                   self.set_logging(12)
            else:
                pass

        #set up the cam feeds and permissions 1 - 4
        if 'cam1' in self.polyConfig['customParams']:
            if str.lower(self.polyConfig['customParams']['cam1']) != 'none':
                self.cam1 = self.polyConfig['customParams']['cam1']
                self.cam2x1feed = True
            else:
                self.cam1 = 'none'

        if 'cam2' in self.polyConfig['customParams']:
            if str.lower(self.polyConfig['customParams']['cam2']) != 'none':
                self.cam2 = self.polyConfig['customParams']['cam2']
                self.cam2x1feed = True
                self.cam2x2feed = True
            else:
                self.cam2 = 'none'

        if 'cam3' in self.polyConfig['customParams']:
            if str.lower(self.polyConfig['customParams']['cam3']) != 'none':
                self.cam3 = self.polyConfig['customParams']['cam3']
                self.cam2x2feed = True
                self.cam3xfeed = True
            else:
                self.cam3 = 'none'

        if 'cam4' in self.polyConfig['customParams']:
            if str.lower(self.polyConfig['customParams']['cam4']) != 'none':
                self.cam4 = self.polyConfig['customParams']['cam4']
                self.cam4xfeed = True
            else:
                self.cam4 = 'none'
                self.cam2x2feed = False

        # set cam feeds 5 - 30
        if 'cam5' in self.polyConfig['customParams']:                # There must be a better way to do this
            self.cam5 = self.polyConfig['customParams']['cam5']
        if 'cam6' in self.polyConfig['customParams']:
            self.cam6 = self.polyConfig['customParams']['cam6']
        if 'cam7' in self.polyConfig['customParams']:
            self.cam7 = self.polyConfig['customParams']['cam7']
        if 'cam8' in self.polyConfig['customParams']:
            self.cam8 = self.polyConfig['customParams']['cam8']
        if 'cam9' in self.polyConfig['customParams']:
            self.cam9 = self.polyConfig['customParams']['cam9']
        if 'cam10' in self.polyConfig['customParams']:
            self.cam10 = self.polyConfig['customParams']['cam10']
        if 'cam11' in self.polyConfig['customParams']:
            self.cam11 = self.polyConfig['customParams']['cam11']
        if 'cam12' in self.polyConfig['customParams']:
            self.cam12 = self.polyConfig['customParams']['cam12']
        if 'cam13' in self.polyConfig['customParams']:
            self.cam13 = self.polyConfig['customParams']['cam13']
        if 'cam14' in self.polyConfig['customParams']:
            self.cam14 = self.polyConfig['customParams']['cam14']
        if 'cam15' in self.polyConfig['customParams']:
            self.cam15 = self.polyConfig['customParams']['cam15']
        if 'cam16' in self.polyConfig['customParams']:
            self.cam16 = self.polyConfig['customParams']['cam16']
        if 'cam17' in self.polyConfig['customParams']:
            self.cam17 = self.polyConfig['customParams']['cam17']
        if 'cam18' in self.polyConfig['customParams']:
            self.cam18 = self.polyConfig['customParams']['cam18']
        if 'cam19' in self.polyConfig['customParams']:
            self.cam19 = self.polyConfig['customParams']['cam19']
        if 'cam20' in self.polyConfig['customParams']:
            self.cam20 = self.polyConfig['customParams']['cam20']
        if 'cam21' in self.polyConfig['customParams']:
            self.cam21 = self.polyConfig['customParams']['cam21']
        if 'cam22' in self.polyConfig['customParams']:
            self.cam22 = self.polyConfig['customParams']['cam22']
        if 'cam23' in self.polyConfig['customParams']:
            self.cam23 = self.polyConfig['customParams']['cam23']
        if 'cam24' in self.polyConfig['customParams']:
            self.cam24 = self.polyConfig['customParams']['cam24']
        if 'cam25' in self.polyConfig['customParams']:
            self.cam25 = self.polyConfig['customParams']['cam25']
        if 'bi_group1' in self.polyConfig['customParams']:
            self.cam26 = self.polyConfig['customParams']['bi_group1']
        if 'bi_group2' in self.polyConfig['customParams']:
            self.cam27 = self.polyConfig['customParams']['bi_group2']
        if 'bi_group3' in self.polyConfig['customParams']:
            self.cam28 = self.polyConfig['customParams']['bi_group3']
        if 'bi_group4' in self.polyConfig['customParams']:
            self.cam29 = self.polyConfig['customParams']['bi_group4']
        if 'bi_group5' in self.polyConfig['customParams']:
            self.cam30 = self.polyConfig['customParams']['bi_group5']

       # setup the triple feed
        if 'triple_feed1' in self.polyConfig['customParams']:
            if 'triple_feed1' in self.polyConfig['customParams']:
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
        # end of camera feed setup

        # setup devices and start options  -------------------------------------------------- bool
        if 'gen_screen_master' in self.polyConfig['customParams']:
            _input = str.lower(self.polyConfig['customParams']['gen_screen_master'])
            if _input == "yes" or _input == "true": self.genScreenConnected = True
            else: self.genScreenConnected = False

        if 'stand_alone' in self.polyConfig['customParams']:
            _input = str.lower(self.polyConfig['customParams']['stand_alone'])
            if _input == "yes" or _input == "true":
                self.standalone = True
                LOGGER.info('Running in Stand Alone Master mode')
            else:
                LOGGER.info('Running in Controller Only mode')

        if 'mm_installed' in self.polyConfig['customParams']:
            _input = str.lower(self.polyConfig['customParams']['mm_installed'])
            if _input == "yes" or _input == "true":
                self.MMinstalled = True
                self.setDriver('GV6', 1)
            else:
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

        if 'sound' in self.polyConfig['customParams']:
            _input = int(self.polyConfig['customParams']['sound'])
            self.setDriver('GV9', _input)
            self.sound = _input
            if self.sound > 0: self.playSound = True
        else:
            self.sound = 0
            self.setDriver('GV9', 0)

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


        # get all the possible custom config options on config page except triple feed
        self.addCustomParam({'cam1': self.cam1, 'cam2': self.cam2, 'cam3': self.cam3, 'cam4': self.cam4,  # required cameras


                             'cam5': self.cam5, 'cam6': self.cam6, 'cam7': self.cam7, 'cam8': self.cam8, 'cam9': self.cam9, 'cam10': self.cam10,
                             'cam11': self.cam11, 'cam12': self.cam12, 'cam13': self.cam13, 'cam14': self.cam14, 'cam15': self.cam15,
                             'cam16': self.cam16, 'cam17': self.cam17, 'cam18': self.cam18, 'cam19': self.cam19, 'cam20': self.cam20,
                             'cam21': self.cam21, 'cam22': self.cam22, 'cam23': self.cam23, 'cam24': self.cam24, 'cam25': self.cam25,

                             'bi_group1': self.cam26, 'bi_group2': self.cam27, 'bi_group3': self.cam28, 'bi_group4': self.cam29, 'bi_group5': self.cam30,

                             'feature_auto_start': self.picFrameAuto, 'cam_screen_level': self.screenLevel, 'cam_screen_timer': self.cam_screen_timer,
                             'feature_screen_level': self.pfscreenLevel, 'pic_frame_timer': self.pic_screen_timer
                           })

        if 'gen_screen_master' in self.polyConfig['customParams']:
            pass
        else:
            LOGGER.info('Adding custom params')
            self.addCustomParam({'sound': 0, 'gen_screen_master': "no", 'stand_alone': "no", 'mm_installed': "no"})
        return True

    ####----------- Start of the fun confusing stuff ----------------------------

    # fire up the stream(s) and show them for the set time
    def setOn(self, command = None):
        self.camFeed = True
        self.runTheFeed = False
        if self.script < 30:
            if self.script == 0:
                feed = self.cam1
            elif self.script == 1:
                feed = self.cam2
            elif self.script == 2:
                feed = self.cam3
            elif self.script == 3:
                feed = self.cam4
            elif self.script == 4:
                feed = self.cam5
            elif self.script == 5:
                feed = self.cam6
            elif self.script == 6:
                feed = self.cam7
            elif self.script == 7:
                feed = self.cam8
            elif self.script == 8:
                feed = self.cam9
            elif self.script == 9:
                feed = self.cam10
            elif self.script == 10:
                feed = self.cam11
            elif self.script == 11:
                feed = self.cam12
            elif self.script == 12:
                feed = self.cam13
            elif self.script == 13:
                feed = self.cam14
            elif self.script == 14:
                feed = self.cam15
            elif self.script == 15:
                feed = self.cam16
            elif self.script == 16:
                feed = self.cam17
            elif self.script == 17:
                feed = self.cam18
            elif self.script == 18:
                feed = self.cam19
            elif self.script == 19:
                feed = self.cam20
            elif self.script == 20:
                feed = self.cam21
            elif self.script == 21:
                feed = self.cam22
            elif self.script == 22:
                feed = self.cam23
            elif self.script == 23:
                feed = self.cam24
            elif self.script == 24:
                feed = self.cam25
            elif self.script == 25:
                feed = self.cam26
            elif self.script == 26:
                feed = self.cam27
            elif self.script == 27:
                feed = self.cam28
            elif self.script == 28:
                feed = self.cam29
            elif self.script == 29:
                feed = self.cam30

            if feed != 'none':
                self.runTheFeed = True
                self.sendSelfCmd(CAM_SCRIPTS[self.script], feed)
                self.sendCloneCmd(CLN_SCRIPTS[self.script])
            else:
                LOGGER.error('No camera is listed in Configuration')

        if self.script ==30 and self.cam2x1feed:
            self.runTheFeed = True
            self.sendSelfCmd(CAM_SCRIPTS[self.script], self.cam1, self.cam2)
            self.sendCloneCmd(CLN_SCRIPTS[self.script])
        elif self.script ==31 and self.cam2x2feed:
            self.runTheFeed = True
            self.sendSelfCmd(CAM_SCRIPTS[self.script], self.cam3, self.cam4)
            self.sendCloneCmd(CLN_SCRIPTS[self.script])
        elif self.script ==32 and self.cam3xfeed:
            self.runTheFeed = True
            self.sendSelfCmd(CAM_SCRIPTS[self.script], self.cam3x_feed1, self.cam3x_feed2, self.cam3x_feed3)
            self.sendCloneCmd(CLN_SCRIPTS[self.script])
        elif self.script ==33 and self.cam4xfeed:
            self.runTheFeed = True
            self.sendSelfCmd(CAM_SCRIPTS[self.script], self.cam1, self.cam2, self.cam3, self.cam4)
            self.sendCloneCmd(CLN_SCRIPTS[self.script])

        # at this point the cam feed command has been sent to master and clones

        if self.runTheFeed:
            LOGGER.info('Running the feed for %s', CLN_SCRIPTS[self.script])
            self.setDriver('GV1', 1)
            self.setDriver('GV2', self.script)
            self.script_running = True
            if not self.genScreenConnected: self.sendSelfCmd(str(self.screenLevel))
            self.sendCloneCmd(str(self.screenLevel))

            #time.sleep(1) # allow a bit to get the feeds going

            if not self.static:
                self.screenOn_timer2() # the timer thread to turn off the screen
            else:
                self.play_sound(self.sound)  # this needs to be faster!!!!!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<
                self.timer_running = True
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
        self.play_sound(self.sound)
        self.timer_running = True
        self.backlight_on()

    def setScript(self, command = None): # from the drop down list
        _script = int(command.get('value'))
        self.script = _script
        self.setDriver('GV2', _script)
        if not self.timer_running:
            self.setOn()
        else:
            if self.show_info_log: LOGGER.info('Still running another timer, skipping')

    def backlight_on(self, command = None):
        if self.screen_on:
            pass
        else:
            if not self.genScreenConnected: self.sendSelfCmd('on')
            elif self.genScreenConnected and not self.picFrameRunning: self.sendSelfCmd('pkill')
            self.sendCloneCmd('on')
            self.screen_on = True
            self.setDriver('GV3', 1)

    def backlight_off(self, command = None): # called from the screenOn_timer to turn off screen if nesseccary
        self.timer_running = False
        if not self.static and self.screen_on and self.picFrameAuto == 0:
            self.setDriver('GV3', 0)
            if self.genScreenConnected:
                self.sb()
            else: self.sendSelfCmd('off')
            if self.screen_on: self.sendCloneCmd('off')
            self.screen_on = False
            self.autoStartPicFrame() #go see if a Feature is selected and installed or enabled
        else:
            self.autoStartPicFrame()

    def backlight_off_manual(self, command = None): # from the controller Screen Off button, toggles the backlight off
        if self.timer_running:
            if self.show_info_log: LOGGER.info('Screen timer running, skipping')
        elif self.screen_on == False:
            if self.show_info_log: LOGGER.info('Screen is already off')
        else:
            self.setDriver('GV3', 0)
            if self.genScreenConnected:
                self.sb()                                           # part of the gen master screem blank
            else:
                self.sendSelfCmd('off')
            self.sendCloneCmd('off')
            self.screen_on = False

    def sbStart(self):                     # called from sb , these are to blank the gen master screen
        self.sendSelfCmd('sb')

    def sb(self):
        self.genMasterSB = True
        sb_thread = threading.Thread(target=self.sbStart)
        sb_thread.daemon = True
        if self.show_debug_log: LOGGER.debug('Blacking out the master screen')
        sb_thread.start()


    def picFrameStart(self): # called from Picture Frame
        _time = str(self.pic_screen_timer)
        _folder = PICTURE_FOLDERS[self.pfFolder]
        if not self.genScreenConnected: self.sendSelfCmd(str(self.pfscreenLevel))
        self.sendSelfCmd('pictureFrame', _time, _folder)

    def pictureFrame(self):
        self.picFrameRunning = True
        if self.show_info_log: LOGGER.info('Starting PictureFrame')
        pic_thread = threading.Thread(target=self.picFrameStart)
        pic_thread.daemon = True
        pic_thread.start()
        time.sleep(4)
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
            if not self.genScreenConnected: self.sendSelfCmd(str(self.pfscreenLevel))
            self.sendCloneCmd(str(self.pfscreenLevel))
            self.backlight_on()
        elif self.picFrameAuto == 3: # camera hold
            self.timer_running = True
        elif self.picFrameAuto == 0:
            self.stopCamFeed()
            self.stopFeature()

    def picFrameAuto(self, command): # triggered by the Optional Feature drop down
        _auto = int(command.get('value'))
        if _auto == 0: # stop any running Feature
            self.picFrameAuto = 0
            self.setDriver('GV12', 0)
            #self.stopFeatureLive()
            if self.timer_running and not self.static:
                self.stopFeatureLive()
            elif self.static:                 #and self.timer_running:
                self.timer_running = False
                self.stopCamFeed()
                self.static = False
                self.backlight_off()
            else:
                self.stopFeature()


        elif _auto == 1: #run Picture Frame
            self.picFrameAuto = 1
            self.setDriver('GV12', 1)
            if self.script_running and not self.timer_running and not self.static: #stop the cam feed
                self.stopCamFeed()
                self.pictureFrame()
            elif self.script_running and self.timer_running and not self.static:
                self.stopFeatureLive()
            elif self.static:
                 self.timer_running = False
                 self.stopCamFeed()
                 self.static = False
                 if self.MMrunning: self.stopFeature()
                 if not self.picFrameRunning: self.pictureFrame()
                 else: self.backlight_on()
            else:
                self.stopFeature()
                self.pictureFrame()

        elif _auto == 2: # run MagicMirror
            if self.MMinstalled:
                self.picFrameAuto = 2
                self.setDriver('GV12', 2)
                if self.script_running and not self.timer_running and not self.static:    #stop the cam feed first
                    self.stopCamFeed()
                    self.startMM()
                elif self.script_running and self.timer_running and not self.static:
                    self.stopFeatureLive()
                elif self.static:
                    self.timer_running = False
                    self.stopCamFeed()
                    self.static = False
                    if self.picFrameRunning:
                        self.stopFeature()
                    if not self.MMrunning:
                        self.startMM()
                    else:
                        if not self.genScreenConnected: self.sendSelfCmd(str(self.pfscreenLevel))
                        self.sendCloneCmd(str(self.pfscreenLevel))
                        self.backlight_on()
                else:
                    self.stopFeature()
                    self.startMM()
            else:
                LOGGER.info('MagicMirror is not installed')

        elif _auto == 3: # screen on with cam feed
            self.setDriver('GV12', 3)
            self.picFrameAuto = 3
            self.static = True
            if self.show_info_log : LOGGER.info('Holding camera feed')
            if self.script_running:
                self.backlight_on()
            else:
                pass
        else: pass

    def stopCamFeed(self, command = None):
        if self.show_info_log: LOGGER.info('Stopping cam feed')
        self.sendSelfCmd('omxkill')
        self.sendCloneCmd('omxkill')
        self.setDriver('GV1', 0)
        self.script_running = False
        self.camFeed = False

    def startMM(self, command = None):
        if self.show_info_log: LOGGER.info('Starting MagicMirror')
        self.sendSelfCmd('MMstart')
        self.sendCloneCmd('MMstart')
        time.sleep(8)             #let MM get started before turning on the backlight
        if not self.genScreenConnected: self.sendSelfCmd(str(self.pfscreenLevel))
        self.sendCloneCmd(str(self.pfscreenLevel))
        self.MMrunning = True
        self.backlight_on()

    def stopFeature(self):
        self.backlight_off_manual()
        self.sendSelfCmd('mkill')
        self.sendCloneCmd('pkill')
        self.MMrunning = False
        self.picFrameRunning = False

    def stopFeatureLive(self):
        self.sendSelfCmd('mkill')
        self.sendCloneCmd('pkill')
        self.MMrunning = False
        self.picFrameRunning = False
        self.genMasterSB = False

    def soundOn(self, command):
        _sound = int(command.get('value'))
        self.sound = _sound
        if _sound > 0:
            self.playSound = True
            self.setDriver('GV9', _sound)
            self.play_sound(_sound)
        else:
            self.playSound = False
            self.setDriver('GV9', 0)

    def play_sound(self, command):
        _sound = command
        if _sound == 0:
            pass

        if _sound > 1 and _sound < 18 :
            if self.playSound and self.standalone: # for the master and clone
                p1 = subprocess.Popen(["aplay", "-q", "/home/pi/.polyglot/nodeservers/PiCamMonitor/Sounds/" + str(SOUNDS[_sound])])
                self.sendCloneCmd('sound' + str(_sound))
                time.sleep(4)
                poll = p1.poll()
            elif self.playSound:                   # for clone only
                self.sendCloneCmd('sound' + str(_sound))

        if _sound  > 0:
            if self.playSound and self.standalone: # for the master and clone
                self.sendCloneCmd('playsound')
                subprocess.call([SPATH + '2tone'])
            elif self.playSound:                   # for clone only
                self.sendCloneCmd('playsound')

    def setScreenOnTime(self, command = None):
        self.cam_screen_timer = int(command.get('value'))
        self.setDriver('GV4', self.cam_screen_timer)

    def setScreenLevel(self, command = None): # sets cam feed level
        self.screenLevel = int(command.get('value'))
        self.setDriver('GV5', self.screenLevel)
        if self.timer_running:
            if not self.genScreenConnected: self.sendSelfCmd(str(self.screenLevel))
            self.sendCloneCmd(str(self.screenLevel))
        else:
            pass

    def picFrameFolder(self, command = None):
        _folder = int(command.get('value'))
        self.setDriver('GV11', _folder)
        self.pfFolder = _folder
        if self.spicFrameAuto == 1 and self.picFrameRunning:
            self.stopFeature()
            self.pictureFrame()
        else:
            pass

    def setPFscreenLevel(self, command = None): # sets feature level
        _level = int(command.get('value'))
        self.pfscreenLevel = _level
        self.setDriver('GV8', _level)
        if not self.timer_running:
            if not self.genScreenConnected: self.sendSelfCmd(str(self.pfscreenLevel))
            self.sendCloneCmd(str(self.pfscreenLevel))
        else:
            pass

    def sendSelfCmd(self, *args):
        _sendIt = True
        _FTL = str(args)
        if not self.camFeed:
            _first2letters = _FTL[2:4]
            if self.genScreenConnected and _first2letters not in GC_LIST:
                _sendIt = False
        if self.standalone and _sendIt:
            try:
                if self.genScreenConnected:
                    r = subprocess.call([XSPATHGEN, *args])
                    #LOGGER.debug('Using the XPATHGEN script') #######################
                else:
                    r = subprocess.call([XSPATH, *args])
                if self.show_debug_log:
                    LOGGER.debug('Master command %s return code %s ', args, r)
            except requests.exceptions.RequestException as e:
                LOGGER.warning('There was a problem with the Master, Error %s ', e)
                return None
            pass
        #self.camFeed = False

    def sendCloneCmd(self, command):
        #_command = command
        if self.clones:
            for node in self.nodes:
                _sendIt = True
                ip = self.nodes[node].getip()
                _online = self.nodes[node].getOnline()
                if ip != None and _online:
                    _generic = self.nodes[node].getGeneric()
                    _sync = self.nodes[node].getSync()
                    if self.ignoreSync: _sync = True
                    #if _generic and command == 'off':
                    #    command = 'sb'
                    #elif _generic and command == 'on':
                    #    command = 'sbkill'
                    #if  _generic == False:
                    #    command = _command
                    _firstTwoLetters = command[:2]
                    if _generic and not _firstTwoLetters in GC_LIST: _sendIt = False

                    if ip != None and _sync and _sendIt:
                        try:
                            if _generic:
                                url = 'http://' + ip + ':6502/cgi-bin/CloneCtrl3gen?' + command
                            else:
                                url = 'http://' + ip + ':6502/cgi-bin/CloneCtrl3?' + command
                            # url = 'http://' + ip + ':6502/cgi-bin/CloneCtrl3?' + command
                            _return =requests.post(url, verify=False, timeout=(10))
                            if self.show_debug_log: LOGGER.debug('Generic = %s, Clone @ %s cmd %s return %s ', _generic, ip, command, _return)
                        except requests.exceptions.RequestException as e:
                            self.nodes[node].setSyncFalse()
                            self.cloneSyncBad = True
                            LOGGER.warning('There was a problem sending the command to Clone %s. Error %s ', ip, e )
                            return None
                else:
                    if ip != None:
                        if self.show_info_log: LOGGER.info('The Clone command %s was skipped for %s because Online is %s ', command, ip, _online)
                    pass

    def clone_thread(self,command):
        pass


    def set_logging(self, command):
        cmdstr = "Info"
        if command == 10: _command = 0
        elif command == 12: _command = 2
        else: _command = int(command.get('value'))

        if _command == 0: cmdstr = "Info"
        if _command == 1: cmdstr = "More Info"
        if _command == 2: cmdstr = "Debug"

        LOGGER.info('Set logging to %s ', cmdstr)
        if _command == 0:
            self.show_debug_log = False
            self.show_info_log = False
            self.setDriver('GV13', 0)
        if _command == 1:
            self.show_info_log = True
            self.show_debug_log = False
            self.setDriver('GV13', 1)
        if _command == 2:
            self.show_debug_log = True
            self.show_info_log = True
            self.setDriver('GV13', 2)

    def shutDownPi(self,command):
        LOGGER.info('Shutting down all Clones')
        self.setDriver('ST', 0)
        self.sendCloneCmd('shutDownPi')

    def piReboot(self,command):
        LOGGER.info('Rebooting all Clones now')
        self.setDriver('ST', 0)
        self.sendCloneCmd('rebootPi')

    def autoCloneSync(self):
        if self.clones:
            LOGGER.warning('A clone is out of sync, Synchronizing....')
            time.sleep(10)
            self.cloneSync()
        else:
            pass

    def cloneSync(self, command = None):
        while self.timer_running:
            time.sleep(1)
        LOGGER.info('Synchronizing the Controller and Clones')
        self.ignoreSync = True
        time.sleep(1)
        for node in self.nodes: self.nodes[node].setSyncTrue()
        for node in self.nodes: self.nodes[node].update()
        time.sleep(1)
        self.sendSelfCmd('killall')
        self.sendCloneCmd('killall')
        time.sleep(1)
        self.backlight_off_manual()
        self.picFrameRunning = False
        self.MMrunning = False
        self.ignoreSync = False
        self.clonesInSync = True
        self.shortPoll()
        self.autoStartPicFrame()

    def set_display(self, command):
        try:
            _query = command.get('query')
            _feature = int(_query.get('OF.uom25'))
            _flevel = int(_query.get('FL.uom56'))
            _screen = int(_query.get('SC.uom2'))
            _sound = int(_query.get('S.uom25'))

            self.picFrameAuto = _feature
            self.setDriver('GV12', _feature)
            self.autoStartPicFrame()
            if _flevel != self.pfscreenLevel and _flevel > 0:
                self.pfscreenLevel = _flevel
                self.setDriver('GV8', _flevel)
            if _screen == True: self.backlight_on()
            elif _screen == False: self.backlight_off_manual()
            self.playSound = True
            self.setDriver('GV9', _sound)
            self.play_sound(_sound)
        except:
            LOGGER.error('There was a problem with the set_display command')
            return False
        return True

    def set_camfeed(self, command):
        if not self.timer_running:
            try:
                _query = command.get('query')
                _feed = int(_query.get('F.uom25'))
                _time = int(_query.get('T.uom56'))
                _sound = int(_query.get('S.uom25'))
                _level = int(_query.get('L.uom56'))

                if _feed != self.script:
                    self.script = _feed
                    self.setDriver('GV2', _feed)
                if _time != self.cam_screen_timer:
                    self.cam_screen_timer = _time
                    self.setDriver('GV4', _time)
                if _sound != self.sound:
                    self.sound = _sound
                    self.setDriver('GV9', _sound)
                if _level != self.screenLevel:
                    self.screenLevel = _level
                    self.setDriver('GV5', _level)
                self.setOn()

            except:
                LOGGER.error('There was a problem with the set_camfeed command')
                return False
            return True
        else:
            if self.show_info_log: LOGGER.info('Skipping, A timer is already running')
            pass

    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all:')
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    def settheflags(self):
        if self.standalone:
            try:
                subprocess.call('sudo chmod -R +x /home/pi/.polyglot/nodeservers/PiCamMonitor/Scripts/', shell=True)
                subprocess.call([SPATH + 'setupfolders.sh', 'normal'])
                subprocess.call([SPATH + 'setupMM.sh', 'normal'])
            except:
                LOGGER.error('There was a problem setting the flags')
                return False
        else:
            pass

    #### --- Necessary defs - Do Not Delete --- ####

    def update(self):
        pass

    def setSyncTrue(self):
        pass

    def CloneCmd(self):
        pass

    def getip(self):
        return None

    def getGeneric(self):
        return False

    def getSync(self):
        return True

    def getOnline(self):
        return True

    def setOffNetwork(self):
        pass

    drivers = [{'driver': 'ST', 'value': 1, 'uom': 2},    #online
               {'driver': 'GV1', 'value': 0, 'uom': 2},   #feed playing
               {'driver': 'GV2', 'value': 0, 'uom': 25},  #feed name
               {'driver': 'GV3', 'value': 0, 'uom': 2},   #screen on
               {'driver': 'GV4', 'value': 0, 'uom': 56},  #cam timer
               {'driver': 'GV5', 'value': 0, 'uom': 56},  #cam bright
               {'driver': 'GV6', 'value': 0, 'uom': 2},   #pf enabled
               {'driver': 'GV7', 'value': 0, 'uom': 56},  #pf timer
               {'driver': 'GV8', 'value': 0, 'uom': 56},  #pf bright
               {'driver': 'GV9', 'value': 0, 'uom': 25},  #sound
               {'driver': 'GV12', 'value': 0, 'uom': 25}, #pf auto
               {'driver': 'GV11', 'value': 0, 'uom': 25}, #pf folder
               {'driver': 'GV13', 'value': 0, 'uom': 25}  #logging level
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
                'SOUND': soundOn,
                'LOGGINGLEVEL': set_logging,
                'CAMFEED': set_camfeed,
                'DISPLAY': set_display
               }

class PingHelper(object):

    def __init__(self, ip, timeout):
        self.ip = ip
        self.timeout = timeout

    def ping(self):
        response = 0
        try:   # RPi
            response,result = subprocess.getstatusoutput("ping -c1 -W " + str(self.timeout) + " " + self.ip)
            if response == 0: return response
        except:
            return None
        if response == 127:
            try:   # Polisy
                response = subprocess.call(['/sbin/ping','-c1','-t' + str(self.timeout), self.ip], shell=False)
                if response == 0: return response
            except:
                return None
        else:
            return None

class CloneNode(polyinterface.Node):
    def __init__(self, controller, primary, address, ipaddress, name):
        super(CloneNode, self).__init__(controller, primary, address, name)
        self.ip = ipaddress
        self.scan = 1
        self.cloneSync = False
        self.online = False
        self.generic = False       # Generic setting

    def start(self):
        self.update

    def update(self):
        if 'gen' in self.name: self.generic = True
        if (self.scan):
            onnet = PingHelper(ip=self.ip,timeout=self.parent.polyConfig['shortPoll']-1)
            result = onnet.ping()
        if (result != None): self.setOnNetwork()
        elif result == None:
            self.setOffNetwork()
            LOGGER.info('Network ' + self.ip + ': Offline')
        else:
            pass

    def setOnNetwork(self):
        self.setDriver('ST', 1)
        self.online = True

    def setOffNetwork(self):
        self.setDriver('ST', 0)
        self.online = False
        self.setSyncFalse()

    def query(self):
        self.update()
        self.reportDrivers()

    def setSyncTrue(self):
        self.cloneSync = True
        self.setDriver('GV1', 1)

    def setSyncFalse(self):
        self.cloneSync = False
        self.setDriver('GV1', 0)

    def getip(self):
        ip = self.ip
        return ip

    def getGeneric(self):       # Generic
        if self.generic == True:
            #time.sleep(.1)
            return True
        else:
            return False

    def getSync(self):
        sync = self.cloneSync
        return sync

    def getOnline(self):
        _online = self.online
        return _online

    def CloneCmd(self,command):
        _sendIt = True
        _firstTwoLetters = command[:2]
        if self.generic and not _firstTwoLetters in GC_LIST: _sendIt = False
        if _sendIt:
            try:
                _ip = str(self.ip)
                url = 'http://' + _ip + ':6502/cgi-bin/CloneCtrl2b?' + command
                requests.get(url)
            except requests.exceptions.RequestException as e:
                self.setSyncFalse()
                self.parent.cloneSyncBad = True
                LOGGER.warning('There was a problem sending the command to Clone %s. Error %s ', ip, e )
                return None
        else:
            pass

    def getSync(self):
        sync = self.cloneSync
        return sync

    def shutDownPi(self,command):
        LOGGER.info('Shutting down the Clone ' + self.address )
        self.setOffNetwork()
        time.sleep(1)
        self.CloneCmd('off')
        self.CloneCmd('shutDownPi')

    def piReboot(self,command):
        LOGGER.info('Rebooting the Clone in 2 seconds ' + self.address )
        self.setOffNetwork()
        time.sleep(1)
        self.CloneCmd('off')
        time.sleep(1)
        self.CloneCmd('rebootPi')

    drivers = [
               {'driver': 'ST', 'value': 0, 'uom': 2},
               {'driver': 'GV1', 'value': 0, 'uom': 2}
              ]

    id = 'clone'

    commands = {
                'SHUT_DOWN': shutDownPi,
                'REBOOT_PI': piReboot,
                'QUERY': query
               }

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('PiCamMonitor')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)

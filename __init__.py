# Copyright 2018 Aditya Mehra (aix.m@outlook.com).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
import re
import sys
import json
import time

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.util import connected, find_input_device
from mycroft.util.log import LOG
from mycroft.util.parse import normalize
from mycroft.audio import wait_while_speaking
from mycroft import intent_file_handler

class XenonPlatform(MycroftSkill):

    IDLE_CHECK_FREQUENCY = 1  # in seconds

    def __init__(self):
        super().__init__("XenonPlatform")

        self.idle_count = 99
        self.override_idle = None
        self.settings['use_listening_beep'] = True

    def initialize(self):
        try:
            # Handle changing the eye color once Mark 1 is ready to go
            # (Part of the statup sequence)
            # Handle the 'waking' visual
            
            self.start_idle_check()
    
            self.add_event('recognizer_loop:audio_output_end', 
                           self.handle_listener_started)
            self.add_event('mycroft.gui.screen.close', self.show_xenon_screen)
            self.gui.register_handler('mycroft.gui.screen.close', 
                                      self.show_xenon_screen)
            
        except Exception:
            LOG.exception('In Xenon Platform Skill')

    #####################################################################
    # Manage "idle" visual state

    def start_idle_check(self):
        # Clear any existing checker
        print("!!!!! START IDLE CHECK !!!!!")
        self.cancel_scheduled_event('IdleCheck')
        self.idle_count = 0
        
        # Schedule a check every few seconds
        self.schedule_repeating_event(self.check_for_idle, None,
                                        XenonPlatform.IDLE_CHECK_FREQUENCY,
                                        name='IdleCheck')

    def check_for_idle(self):
        self.idle_count += 1
        
        if self.idle_count == 5:
            # Go into a 'sleep' visual state
            #self.show_xenon_screen()
            self.gui.send_event('mycroft.gui.close.screen', {})
        elif self.idle_count > 5:
            self.cancel_scheduled_event('IdleCheck')

    def handle_listener_started(self, message):
        if False:
            self.cancel_scheduled_event('IdleCheck')
        else:
            print("IDLE CHECK!")
            # Check if in 'idle' state and visually come to attention
            if self.idle_count > 2:
                # Perform 'waking' animation
                # TODO: Anything in QML?  E.g. self.gui.show_page("waking.qml")

                # Begin checking for the idle state again
                self.idle_count = 0
                self.start_idle_check()
                
    def show_xenon_screen(self):
        """ When listening has ended show the thinking animation. """
        print("sent back")
        self.gui.send_event('mycroft.gui.close.screen', {})
        #self.gui.show_page('blank.qml')
        
def create_skill():
    return XenonPlatform()

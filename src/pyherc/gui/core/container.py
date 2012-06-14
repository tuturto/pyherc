#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
#
#   This file is part of pyherc.
#
#   pyherc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyherc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

"""
Module for container
"""
import pgu.gui
import pygame
from pygame.locals import JOYAXISMOTION, JOYBUTTONUP

class Container(pgu.gui.Container):
    """
    Specialised container widget that knows how to handle joypad
    """
    def __init__(self, **params):
        """
        Default constructor
        """
        super(Container, self).__init__(**params)

        self.time = pygame.time.get_ticks()

        #TODO: move to outside
        pygame.joystick.init()
        joy = pygame.joystick.Joystick(1)
        joy.init()
        print joy

        #self.connect(JOYAXISMOTION, self.joystick_event)
        # elif e.key == K_DOWN:
        # self._move_focus(0,1)
        # return True

    def joystick_event(self, code, event):
        if self.time + 250 > pygame.time.get_ticks():
            return
        else:
            self.time = pygame.time.get_ticks()
        print event
        if event.type == JOYAXISMOTION:
            if event.axis == 1:
                if event.value > 0.5:
                    self._move_focus(0, 1)
                elif event.value < -0.5:
                    self._move_focus(0, -1)

    def send(self, code, event = None):
        if event != None and event.type in (JOYAXISMOTION, JOYBUTTONUP):
            self.joystick_event(code, event)
        super(Container, self).send(code, event)

    def _event(self,e):
        super(Container, self)._event(e)

    def event(self, event):
        """
        Handle events
        """
        used = super(Container, self).event(event)

        return used

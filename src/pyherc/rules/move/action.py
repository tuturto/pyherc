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
Module defining classes related to Move
"""
from pyherc.events import MoveEvent
from pyherc.aspects import logged

class MoveAction(object):
    """
    Action for moving
    """
    @logged
    def __init__(self, character, new_location, new_level = None):
        """
        Default constructor

        :param character: character moving
        :type character: Character
        :param new_location: location to move
        :type new_location: (int, int)
        :param new_level: level to move
        :type new_level: Level
        """
        self.character = character
        self.new_location = new_location
        self.new_level = new_level
        self.model = None

    @logged
    def execute(self):
        """
        Executes this Move
        """
        if self.is_legal():

            affected_tiles = [self.character.location,
                              self.new_location]

            self.character.location = self.new_location
            if self.new_level != None:
                if self.character.level != self.new_level:
                    self.character.level.remove_creature(self.character)
                    self.character.level = self.new_level
                    self.new_level.add_creature(self.character,
                                                self.new_location)
            self.character.add_to_tick(2)

            self.character.raise_event(MoveEvent(
                                            mover = self.character,
                                            affected_tiles = affected_tiles))

        else:
            self.character.add_to_tick(1)

    @logged
    def is_legal(self):
        """
        Check if the move is possible to perform

        :returns: True if move is possible, false otherwise
        :rtype: Boolean
        """
        location_ok = False
        if self.new_level != None:
            if not self.new_level.blocks_movement(self.new_location[0],
                                                  self.new_location[1]):
                #check for other creatures and such
                location_ok = True
                creatures = self.new_level.creatures
                for creature in creatures:
                    if creature.location == self.new_location:
                        location_ok = False
            else:
                location_ok = False
        else:
            pass

        return location_ok

class WalkAction(MoveAction):
    """
    Action for walking
    """
    def execute(self):
        """
        Execute this move
        """
        MoveAction.execute(self)

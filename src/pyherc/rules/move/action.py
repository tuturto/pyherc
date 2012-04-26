#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2011 Tuukka Turto
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
Module defining classes related to MoveAttack
"""
import logging
import pyherc.rules.time

class MoveAction():
    """
    Action for moving
    """
    def __init__(self, character, new_location, new_level = None):
        """
        Default constructor

        Args:
            character: Character moving
            new_location: Location to move
        """
        self.logger = logging.getLogger('pyherc.rules.move.action.MoveAction')
        self.character = character
        self.new_location = new_location
        self.new_level = new_level
        self.model = None

    def execute(self):
        """
        Executes this Move
        """
        if self.is_legal():
            self.character.location = self.new_location
            if self.new_level != None:
                if self.character.level != self.new_level:
                    self.character.level.remove_creature(self.character)
                    self.character.level = self.new_level
                    self.new_level.add_creature(self.character,
                                                self.new_location)
            self.character.add_to_tick(2)
        else:
            self.logger.warn('Tried to execute illegal move')
            self.character.add_to_tick(2)

    def is_legal(self):
        """
        Check if the move is possible to perform

        Returns:
            True if move is possible, false otherwise
        """
        location_ok = False
        if self.new_level != None:
            if self.new_level.walls[self.new_location[0]][self.new_location[1]] == pyherc.data.tiles.WALL_EMPTY:
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

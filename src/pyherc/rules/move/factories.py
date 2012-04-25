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
Attack related factories are defined here
"""
import types
import logging
import pyherc.data.tiles
from pyherc.rules.move.action import MoveAction
from pyherc.rules.factory import SubActionFactory

class WalkFactory(SubActionFactory):
    """
    Factory for creating walk actions
    """
    def __init__(self):
        """
        Constructor for this factory
        """
        self.logger = logging.getLogger('pyherc.rules.move.factories.WalkFactory')
        self.movement_mode = 'walk'

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        data = dict(self.__dict__)
        del data['logger']
        return data

    def __setstate__(self, data):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(data)
        self.logger = logging.getLogger('pyherc.rules.move.factories.WalkFactory')

    def __str__(self):
        return 'walk factory'

    def can_handle(self, parameters):
        """
        Can this factory process these parameters

        Args:
            parameters: Parameters to check

        Returns:
            True if factory is capable of handling parameters
        """
        return self.movement_mode == parameters.movement_mode

    def get_action(self, parameters):
        """
        Create a walk action

        Args:
            parameters: Parameters used to control walk creation
        """
        location = parameters.character.location
        new_level = parameters.character.level
        direction = parameters.direction
        new_location = None

        if direction == 1:
            new_location = (location[0], location[1] - 1)
        elif direction == 2:
            new_location = (location[0] + 1, location[1] - 1)
        elif direction == 3:
            new_location = (location[0] + 1, location[1])
        elif direction == 4:
            new_location = (location[0] + 1, location[1] + 1)
        elif direction == 5:
            new_location = (location[0], location[1] + 1)
        elif direction == 6:
            new_location = (location[0] - 1, location[1] + 1)
        elif direction == 7:
            new_location = (location[0] - 1, location[1])
        elif direction == 8:
            new_location = (location[0] - 1, location[1] - 1)
        elif direction == 9:
            portal = new_level.get_portal_at(location)
            if portal != None:
                if portal.other_end != None:
                    new_level = portal.other_end.level
                    new_location = portal.other_end.location
                else:
                    self.logger.error('Portal leads to void!')
                    raise RuntimeError('Portal leads to void!')
            else:
                new_level = parameters.character.level
                new_location = parameters.character.location

        #is new location blocked?
        if new_level.get_wall_tile(new_location[0], new_location[1]) != pyherc.data.tiles.WALL_EMPTY:
            new_location = parameters.character.location

        return MoveAction(parameters.character, new_location, new_level)

class MoveFactory(SubActionFactory):
    """
    Factory for constructing move actions
    """
    def __init__(self, factories):
        """
        Constructor for this factory

        Args:
            factories: a single Factory or list of Factories to use
        """
        self.logger = logging.getLogger('pyherc.rules.move.factories.MoveFactory')
        self.action_type = 'move'

        if isinstance(factories, types.ListType):
            self.factories = factories
        else:
            self.factories = []
            self.factories.append(factories)

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        data = dict(self.__dict__)
        del data['logger']
        return data

    def __setstate__(self, data):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(data)
        self.logger = logging.getLogger('pyherc.rules.move.factories.MoveFactory')

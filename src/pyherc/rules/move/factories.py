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
Attack related factories are defined here
"""
import types
from pyherc.aspects import logged
from pyherc.rules.move.action import MoveAction, EscapeAction
from pyherc.rules.factory import SubActionFactory

class WalkFactory(SubActionFactory):
    """
    Factory for creating walk actions
    """
    @logged
    def __init__(self, level_generator_factory):
        """
        Constructor for this factory

        :param level_generator_factory: Factory for generating level generators
        :type level_generator_factory: LevelGeneratorFactory
        """
        self.level_generator_factory = level_generator_factory
        self.movement_mode = 'walk'

    def __str__(self):
        return 'walk factory'

    @logged
    def can_handle(self, parameters):
        """
        Can this factory process these parameters

        :param parameters: Parameters to check
        :type parameters: MoveParameters

        :returns: True if factory is capable of handling parameters
        :rtype: boolean
        """
        return self.movement_mode == parameters.movement_mode

    @logged
    def get_action(self, parameters):
        """
        Create a walk action

        :param parameters: Parameters used to control walk creation
        :type parameters: MoveParameters
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
                if not portal.exits_dungeon:
                    other_end = portal.get_other_end(self.level_generator_factory)
                    if other_end != None:
                        new_level = other_end.level
                        new_location = other_end.location
                    else:
                        raise RuntimeError('Portal leads to void!')
                else:
                    return EscapeAction(parameters.character)
            else:
                new_level = parameters.character.level
                new_location = parameters.character.location
        else:
            raise RuntimeError('Character does not know where to go')

        #is new location blocked?
        if new_level.blocks_movement(new_location[0], new_location[1]):
            new_location = parameters.character.location

        return MoveAction(parameters.character, new_location, new_level)

class MoveFactory(SubActionFactory):
    """
    Factory for constructing move actions
    """
    @logged
    def __init__(self, factories):
        """
        Constructor for this factory

        :param factories: a single Factory or list of Factories to use
        """
        self.action_type = 'move'

        if hasattr(factories, '__iter__'):
            self.factories = factories
        else:
            self.factories = []
            self.factories.append(factories)

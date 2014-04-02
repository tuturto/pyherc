# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
import random

from pyherc.aspects import log_debug, log_info
from pyherc.rules.factory import SubActionFactory
from pyherc.rules.moving.action import (EscapeAction, MoveAction,
                                        SwitchPlacesAction)


class WalkFactory(SubActionFactory):
    """
    Factory for creating walk actions
    """
    @log_debug
    def __init__(self, level_generator_factory, dying_rules):
        """
        Constructor for this factory

        :param level_generator_factory: Factory for generating level generators
        :type level_generator_factory: LevelGeneratorFactory
        """
        super().__init__()
        self.level_generator_factory = level_generator_factory
        self.dying_rules = dying_rules
        self.movement_mode = 'walk'

    @log_debug
    def __str__(self):
        return 'walk factory'

    @log_debug
    def can_handle(self, parameters):
        """
        Can this factory process these parameters

        :param parameters: Parameters to check
        :type parameters: MoveParameters

        :returns: True if factory is capable of handling parameters
        :rtype: boolean
        """
        return self.movement_mode == parameters.movement_mode

    @log_info
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
            return self._get_action_for_portal(parameters.character)
        else:
            raise RuntimeError('Character does not know where to go')

        if new_level.blocks_movement(new_location[0], new_location[1]):
            new_location = parameters.character.location
        elif new_level.get_creature_at(new_location):
            return self.get_place_switch_action(parameters.character,
                                                new_location)

        return MoveAction(character=parameters.character,
                          new_location=new_location,
                          new_level=new_level,
                          skip_creature_check=False,
                          dying_rules=self.dying_rules)

    @log_debug
    def get_place_switch_action(self, character, new_location):
        """
        Get action for two character switching places

        .. versionadded:: 0.11
        """
        other_character = character.level.get_creature_at(new_location)

        return SwitchPlacesAction(character,
                                  other_character,
                                  self.dying_rules)

    @log_debug
    def _get_action_for_portal(self, character):
        """
        Get location after entering a portal

        :returns: action for entering portal
        :rtype: Action

        .. versionadded:: 0.11

        .. note:: Entering portal may lead player next to other end if it is
                  blocked by other character
        """
        location = character.location
        new_level = character.level
        new_location = None

        portal = new_level.get_portal_at(location)
        if portal is not None:
            if not portal.exits_dungeon:
                other_end = portal.get_other_end(self.level_generator_factory)
                if other_end is not None:
                    new_level = other_end.level
                    new_location = self._area_around_portal(other_end)
                else:
                    raise RuntimeError('Portal leads to void!')
            else:
                return EscapeAction(character)
        else:
            new_level = character.level
            new_location = character.location

        return MoveAction(character,
                          new_location,
                          new_level,
                          False,
                          self.dying_rules)

    @log_debug
    def _area_around_portal(self, portal):
        """
        Get passable tiles in 3x3 area around a portal
        """
        level = portal.level
        location = portal.location

        if not (level.blocks_movement(location[0], location[1]) or
                level.get_creature_at(location)):
            return location

        passables = []

        for loc_x in range(location[0]-1, location[1]+1):
            for loc_y in range(location[1]-1, location[1]+1):
                if not (level.blocks_movement(loc_x, loc_y) or
                        level.get_creature_at((loc_x, loc_y))):
                    passables.append((loc_x, loc_y))

        return random.choice(passables)


class MoveFactory(SubActionFactory):
    """
    Factory for constructing move actions
    """
    @log_debug
    def __init__(self, factories):
        """
        Constructor for this factory

        :param factories: a single Factory or list of Factories to use
        """
        super().__init__()
        self.action_type = 'move'

        if hasattr(factories, '__iter__'):
            self.factories = factories
        else:
            self.factories = []
            self.factories.append(factories)

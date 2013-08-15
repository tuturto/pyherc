#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
AI routines for skeletons
"""

from pyherc.aspects import log_debug
from pyherc.ai.pathfinding import a_star
from pyherc.events import NoticeEvent, LoseFocusEvent

class SkeletonWarriorAI():
    """
    AI for skeleton warrior

    ..versionadded:: 0.7
    """
    @log_debug
    def __init__(self, character):
        """
        Default constructor

        :param character: character to connect
        :type character: Character
        """
        self.character = character

        self.mode = 'patrol'
        self.destination = None

    @log_debug
    def act(self, model, action_factory, rng):
        """
        Trigger this AI to assess the situation and act accordingly

        :param model: model where the character is located
        :type model: Model
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory
        :param rng: random number generator
        :type rng: Random
        """
        del self.character.short_term_memory[:]

        if self.character.inventory.weapon == None:
            self._wield_weapon(action_factory)

        c_location = self.character.location
        p_location = model.player.location

        distance = ((c_location[0] - p_location[0]) ** 2 +
                    (c_location[1] - p_location[1]) ** 2) ** 0.5

        if distance < 4:
            if self.mode != 'combat':
                self.character.raise_event(
                                    NoticeEvent(character = self.character,
                                                target = model.player))
            self.mode = 'combat'
        else:
            if self.mode != 'patrol':
                self.character.raise_event(
                                LoseFocusEvent(character = self.character))
            self.mode = 'patrol'

        if self.mode == 'patrol':
            self._patrol(model, action_factory, rng)
        else:
            self._combat(model, action_factory, rng)

    @log_debug
    def _wield_weapon(self, action_factory):
        """
        Check if it is possible to wield a weapon and do so
        """
        weapons = [item for item in
                   self.character.inventory
                   if item.weapon_data != None]

        self.character.equip(weapons[0],
                             action_factory)

    @log_debug
    def _patrol(self, model, action_factory, rng):
        """
        Patrol around the level
        """
        character = self.character
        level = self.character.level

        while (self.destination == None
               or character.location == self.destination):

            self.destination = level.find_free_space()

        path, connections, updated = a_star(character.location,
                                            self.destination,
                                            level)

        next_tile = path[1]

        direction = self.find_direction(character.location,
                                        next_tile)

        if character.is_move_legal(direction,
                                   'walk',
                                   action_factory):
            character.move(direction,
                           action_factory)
        else:
            character.tick = character.tick + 10

    @log_debug
    def _combat(self, model, action_factory, rng):
        """
        Attack enemies
        """
        character = self.character
        player = model.player
        c_location = character.location
        p_location = player.location

        distance = ((c_location[0] - p_location[0]) ** 2 +
                    (c_location[1] - p_location[1]) ** 2) ** 0.5

        if distance < 1.42:
            direction = self.find_direction(c_location,
                                            p_location)
            character.perform_attack(direction,
                                     action_factory,
                                     rng)
        else:
            path, connections, updated = a_star(c_location,
                                                p_location,
                                                character.level)
            next_tile = path[1]

            direction = self.find_direction(character.location,
                                            next_tile)

            if character.is_move_legal(direction,
                                       'walk',
                                       action_factory):
                character.move(direction,
                               action_factory)
            else:
                character.tick = character.tick + 10

    @log_debug
    def find_direction(self, start, end):
        """
        Find direction from start to end

        :param start: start location
        :type start: (integer, integer)
        :param end: end location
        :type end: (integer, integer)

        :returns: Direction to travel
        :rtype: integer
        """
        assert(start != None)
        assert(end != None)

        direction = None
        if start[0] < end[0]:
            #right side
            if start[1] < end[1]:
                #right, below
                direction = 4
            elif start[1] > end[1]:
                #right, above
                direction = 2
            else:
                #right
                direction = 3
        elif start[0] > end[0]:
            #left side
            if start[1] < end[1]:
                #left, below
                direction = 6
            elif start[1] > end[1]:
                #left, above
                direction = 8
            else:
                #left
                direction = 7
        else:
            #up or down
            if start[1] < end[1]:
                #below
                direction = 5
            elif start[1] > end[1]:
                #above
                direction = 1

        return direction

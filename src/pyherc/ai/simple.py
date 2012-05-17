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
Simple AI for flocking creature

Creature will try to find friends, before attacking the player character
"""

import math
from pyherc.aspects import Logged

class FlockingHerbivore(object):
    """
    AI for flocking herbivore
    Tries to maintain close distance to other animals
    Seeks out player for combat
    """

    logged = Logged()

    @logged
    def __init__(self, character):
        """
        Default constructor

        :param character: character to connect
        :type character: Character
        """
        self.character = character

    @logged
    def act(self, model):
        """
        Trigger this AI to assess the situation and act accordingly

        :param model: model where the character is located
        :type model: Model
        """
        shortest_distance = None
        closest_creature = None
        character = self.character
        player = model.player

        del character.short_term_memory[:]

        for creature in character.level.creatures:
            if creature != character:
                loc_x = abs(creature.location[0] - character.location[0])
                loc_y = abs(creature.location[1] - character.location[1])
                distance = math.sqrt(loc_x * loc_x + loc_y * loc_y)
                if shortest_distance != None:
                    if distance < shortest_distance:
                        shortest_distance = distance
                        closest_creature = creature
                else:
                    shortest_distance = distance
                    closest_creature = creature

        if shortest_distance != None:
            if shortest_distance <= 2:
                #seek player instead
                loc_x = abs(player.location[0] - character.location[0])
                loc_y = abs(player.location[1] - character.location[1])
                distance = math.sqrt(loc_x * loc_x + loc_y * loc_y)

                direction = self.find_direction(
                                        character.location, player.location)

                if distance > 1:
                    if character.is_move_legal(direction, 'walk'):
                        character.move(direction)
                    else:
                        character.tick = character.tick + 10
                else:
                    #attack
                    character.perform_attack(direction)
            else:
                #find direction
                direction = self.find_direction(character.location,
                                                    closest_creature.location)
                if character.is_move_legal(direction, 'walk'):
                    character.move(direction)
                else:
                    character.tick = character.tick + 10
        else:
            #we're all alone here
            character.tick = character.tick + 10

    @logged
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

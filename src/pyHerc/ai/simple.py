#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

'''
Simple AI for flocking creature

Creature will try to find friends, before attacking the player character
'''

import math
import pyHerc.rules.moving
import pyHerc.rules.combat
from pyHerc.rules.public import MoveParameters
from pyHerc.rules.public import AttackParameters

class FlockingHerbivore():
    """
    AI for flocking herbivore
    Tries to maintain close distance to other animals
    Seeks out player for combat
    """

    def __init__(self, character):
        self.character = character

    def act(self, model):
        '''
        Trigger this AI to assess the situation and act accordingly
        '''
        shortest_distance = None
        closest_creature = None
        character = self.character
        player = model.player

        #TODO: handle memory
        del self.character.short_term_memory[:]

        for creature in self.character.level.creatures:
            if creature != self.character:
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

                if distance > 1:
                    direction = self.find_direction(
                                        character.location, player.location)

                    action = self.character.create_action(
                                MoveParameters(character, direction, 'walk')
                                )
                    if action.is_legal() == True:
                        action.execute()
                    else:
                        self.character.tick = self.character.tick + 10
                else:
                    #attack
                    character.execute_action(
                                    AttackParameters(character, player, 'unarmed')
                                    )
                    # pyHerc.rules.combat.melee_attack(model, character, player)
            else:
                #find direction
                direction = self.find_direction(character.location,
                                                    closest_creature.location)

                action = self.character.create_action(
                                    MoveParameters(character, direction, 'walk')
                                    )
                if action.is_legal() == True:
                    action.execute()
                else:
                    self.character.tick = self.character.tick + 10
        else:
            #we're all alone here
            self.character.tick = self.character.tick + 10

    def find_direction(self, start, end):
        """
        Find direction from start to end
        @param start: start location
        @param end: end location
        @return: Direction to travel
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

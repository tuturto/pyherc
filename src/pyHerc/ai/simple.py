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

def flocking_herbivore(self, model):
    """
    AI for flocking herbivore
    Tries to maintain close distance to other animals
    Seeks out player for combat
    """
    shortest_distance = None
    closest_creature = None

    #TODO: handle memory
    del self.short_term_memory[:]

    for creature in self.level.creatures:
        if creature != self:
            loc_x = abs(creature.location[0] - self.location[0])
            loc_y = abs(creature.location[1] - self.location[1])
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
            loc_x = abs(model.player.location[0] - self.location[0])
            loc_y = abs(model.player.location[1] - self.location[1])
            distance = math.sqrt(loc_x * loc_x + loc_y * loc_y)

            if distance > 1:
                direction = find_direction(self.location, model.player.location)
                result = pyHerc.rules.moving.check_move(model, self, direction)
                if result['ok']:
                    pyHerc.rules.moving.move(model, self, direction)
                else:
                    self.tick = self.tick + 10
            else:
                #attack
                pyHerc.rules.combat.melee_attack(model, self, model.player)
        else:
            #find direction
            direction = pyHerc.ai.simple.find_direction(self.location,
                                                       closest_creature.location)
            result = pyHerc.rules.moving.check_move(model, self, direction)
            if result['ok']:
                pyHerc.rules.moving.move(model, self, direction)
            else:
                self.tick = self.tick + 10
    else:
        #we're all alone here
        self.tick = self.tick + 10

def find_direction(start, end):
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

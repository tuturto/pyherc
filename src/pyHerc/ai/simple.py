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

import math
import pyHerc.ai.simple
import pyHerc.rules.moving
import pyHerc.rules.combat

def proofOfConcept(self, model):
    """
    Proof of concept
    This AI will just utter words "hello World"
    Not to be used with the actual game
    """
    print('hello world')
    self.tick = self.tick + 10

def flockingHerbivore(self, model):
    """
    AI for flocking herbivore
    Tries to maintain close distance to other animals
    Seeks out player for combat
    """
    shortestDistance = None
    closestCreature = None

    #TODO: handle memory
    del self.shortTermMemory[:]

    for creature in self.level.creatures:
        if creature != self:
            x = abs(creature.location[0] - self.location[0])
            y = abs(creature.location[1] - self.location[1])
            distance = math.sqrt(x * x + y * y)
            if shortestDistance != None:
                if distance < shortestDistance:
                    shortestDistance = distance
                    closestCreature = creature
            else:
                shortestDistance = distance
                closestCreature = creature

    if shortestDistance != None:
        if shortestDistance <= 2:
            #seek player instead
            x = abs(model.player.location[0] - self.location[0])
            y = abs(model.player.location[1] - self.location[1])
            distance = math.sqrt(x * x + y * y)

            if distance > 1:
                direction = findDirection(self.location, model.player.location)
                result = pyHerc.rules.moving.checkMove(model, self, direction)
                if result['ok']:
                    pyHerc.rules.moving.move(model, self, direction)
                else:
                    self.tick = self.tick + 10
            else:
                #attack
                pyHerc.rules.combat.meleeAttack(model, self, model.player)
        else:
            #find direction
            direction = pyHerc.ai.simple.findDirection(self.location, closestCreature.location)
            result = pyHerc.rules.moving.checkMove(model, self, direction)
            if result['ok']:
                pyHerc.rules.moving.move(model, self, direction)
            else:
                self.tick = self.tick + 10
    else:
        #we're all alone here
        self.tick = self.tick + 10

def findDirection(start, end):
    """
    Find direction from start to end
    Parameters:
        start : start location
        end : end location
    Returns:
        Direction to travel
    """
    assert(start != None)
    assert(end != None)

    if start[0] < end[0]:
        #right side
        if start[1] < end[1]:
            #right, below
            return 4
        elif start[1] > end[1]:
            #right, above
            return 2
        else:
            #right
            return 3
    elif start[0] > end[0]:
        #left side
        if start[1] < end[1]:
            #left, below
            return 6
        elif start[1] > end[1]:
            #left, above
            return 8
        else:
            #left
            return 7
    else:
        #up or down
        if start[1] < end[1]:
            #below
            return 5
        elif start[1] > end[1]:
            #above
            return 1

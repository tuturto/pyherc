# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Simple AI for flocking creature

Creature will try to find friends, before attacking the player character
"""

import math

from pyherc.aspects import log_debug
from pyherc.data.geometry import find_direction
from pyherc.rules import attack, is_move_legal, move


class FlockingHerbivore():
    """
    AI for flocking herbivore
    Tries to maintain close distance to other animals
    Seeks out player for combat
    """
    @log_debug
    def __init__(self, character):
        """
        Default constructor

        :param character: character to connect
        :type character: Character
        """
        self.character = character

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

                direction = find_direction(character.location,
                                           player.location)

                if distance > 1.42:
                    if is_move_legal(character,
                                     direction,
                                     'walk',
                                     action_factory):
                        move(character, direction, action_factory)
                    else:
                        character.tick = character.tick + 10
                else:
                    #attack
                    attack(character,
                           direction,
                           action_factory,
                           rng)
            else:
                #find direction
                direction = find_direction(character.location,
                                           closest_creature.location)
                if is_move_legal(character,
                                 direction,
                                 'walk',
                                 action_factory):
                    move(character, direction, action_factory)
                else:
                    character.tick = character.tick + 10
        else:
            #we're all alone here
            character.tick = character.tick + 10

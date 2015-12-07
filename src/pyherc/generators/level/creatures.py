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
Classes for creature generation
"""

from pyherc.aspects import log_debug, log_info
from pyherc.data import (add_character, get_locations_by_tag, blocks_movement,
                         safe_passage)


class CreatureAdder():
    """
    Class used to add creatures during level generation
    """
    @log_debug
    def __init__(self, creatures, configuration, rng):
        """
        Default constructor

        :param creature_generator: creature generator used to create creatures
        :type creature_generator: CreatureGenerator
        :param configuration: configuration
        :type configuration: CreatureAdderConfiguration
        :param rng: random number generator
        :type rng: Random
        """
        super().__init__()
        self.creatures = creatures
        self.configuration = configuration
        self.rng = rng

    @log_debug
    def __get_level_types(self):
        """
        Get level types this adder can be used at

        :returns: level types this adder can be used at
        :rtype: [string]
        """
        return self.configuration.level_types

    def __call__(self, level):
        """
        Add creatures to level according to configuration
        """
        self.add_creatures(level)

    @log_info
    def add_creatures(self, level):
        """
        Add creatures to level according to configuration

        :param level: level to add creatures
        :type level: Level
        """
        creatures = []

        for creature in self.configuration:
            amount = self.rng.randint(creature['min_amount'],
                                      creature['max_amount'])
            creatures.extend(self.generate_creatures(creature['name'],
                                                     amount))

        self.place_creatures(creatures, self.configuration, level)

    @log_debug
    def generate_creatures(self, name, amount):
        """
        Generate creatures

        :param name: name of the creatures to generate
        :type name: string
        :param amount: amount of creatures to generate
        :type amount: integer
        :returns: generated creatures
        :rtype: [Character]
        """
        creatures = []
        for i in range(amount):
            new_creature = self.creatures(name)
            creatures.append(new_creature)

        return creatures

    @log_debug
    def place_creatures(self, creatures, creature_list, level):
        """
        Place creatures into a level

        :param creatures: creatures to place
        :type creatures: [Character]
        :param creature_list: specification where to place creatures
        :type creature_list: dict
        :param level: level to place creatures
        :type level: Level
        """
        for creature in creatures:
            location_types = [x['location'] for x in creature_list
                              if x['name'] == creature.name]

            if not location_types:
                location_types = ['any']
               

            locations = []
            for location_type in location_types:
                locations.extend([location for location in (get_locations_by_tag(level,
                                                                                 location_type))
                                  if safe_passage(level, location)])

            if locations:
                location = self.rng.choice(locations)
                add_character(level, location, creature)

    level_types = property(__get_level_types)

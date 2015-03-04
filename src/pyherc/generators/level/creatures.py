# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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
Classes for creature generation
"""

from pyherc.aspects import log_debug, log_info
from pyherc.data import (add_character, get_locations_by_tag, blocks_movement,
                         get_trap)


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
            location_type = [x['location'] for x in creature_list
                             if x['name'] == creature.name]

            if location_type is None:
                location_type = 'any'

            def suitable_location(location):
                if blocks_movement(level, location):
                    return False
                if get_trap(level, location):
                    return False
                return True

            locations = [location for location in (get_locations_by_tag(level, 'room'))
                         if suitable_location(location)]

            if locations:
                location = self.rng.choice(locations)
                add_character(level, location, creature)

    level_types = property(__get_level_types)

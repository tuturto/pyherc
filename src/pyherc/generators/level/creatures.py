#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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

class CreatureAdderConfiguration(object):
    """
    Class used to configure CreatureAdder
    """
    def __init__(self, level_types):
        """
        Default constructor

        Args:
            level_types: types of levels adder can be used at
        """
        super(CreatureAdderConfiguration, self).__init__()
        self.level_types = level_types
        self.creature_list = []

    def add_creature(self, min_amount, max_amount, name, location = None):
        """
        Adds creature specification

        Args:
            min_amount: Minimum amount of creatures to generate
            max_amount: Maximum amount of creatures to generate
            name: Name of the creature to generate
            location: location type where creature is placed
        """
        config_item = {}
        config_item['min_amount'] = min_amount
        config_item['max_amount'] = max_amount
        config_item['name'] = name
        config_item['location'] = location

        self.creature_list.append(config_item)

class CreatureAdder(object):
    """
    Class used to add creatures during level generation
    """
    def __init__(self, creature_generator, configuration, rng):
        """
        Default constructor

        Args:
            creature_generator: CreatureGenerator used to create creatures
            configuration: CreatureAdderConfiguration
            rng: random number generator
        """
        super(CreatureAdder, self).__init__()
        self.creature_generator = creature_generator
        self.configuration = configuration
        self.rng = rng

    def __get_level_types(self):
        """
        Get level types this adder can be used at
        """
        return self.configuration.level_types

    def add_creatures(self, level):
        """
        Add creatures to level according to configuration

        Args:
            level: Level to add creatures
        """
        creature_list = self.configuration.creature_list
        creatures = []

        for creature in creature_list:
            amount = self.rng.randint(creature['min_amount'],
                                      creature['max_amount'])
            creatures.extend(self.generate_creatures(creature['name'],
                                                     amount))

        self.place_creatures(creatures, creature_list, level)

    def generate_creatures(self, name, amount):
        """
        Generate creatures

        Args:
            name: Name of the creatures to generate
            amount: Amount of creatures to generate

        Returns:
            List of generated creatures
        """
        creatures = []
        params = {}
        params['name'] = name
        for i in range(amount):
            new_creature = self.creature_generator.generate_creature(params)
            creatures.append(new_creature)

        return creatures

    def place_creatures(self, creatures, creature_list, level):
        """
        Place creatures into a level

        Args:
            creatures: List of Creatures to place
            creature_list: specification where to place creatures
            level: Level to place creatures
        """
        for creature in creatures:
            location_type = [x['location'] for x in creature_list
                             if x['name'] == creature.name]

            if location_type == None:
                location_type = 'any'

            locations = level.get_locations_by_type('room')

            location = self.rng.choice(locations)

            level.add_creature(creature, location)

    level_types = property(__get_level_types)


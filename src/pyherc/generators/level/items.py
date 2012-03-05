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
Classes for item generation
"""
from pyherc.aspects import Logged

class ItemAdderConfiguration(object):
    """
    Configuration for ItemAdder
    """
    __logger_name__ = 'pyherc.generators.level.items.ItemAdderConfiguration'

    @Logged(__logger_name__)
    def __init__(self, level_types):
        """
        Default constructor
        """
        super(ItemAdderConfiguration, self).__init__()
        self.level_types = level_types
        self.items = []

    @Logged(__logger_name__)
    def add_item(self, min_amount, max_amount, name = None, type = None,
                 location = None):
        """
        Adds item to configuration

        Args:
            item: specification for item
        """
        item_spec = {}
        item_spec['min_amount'] = min_amount
        item_spec['max_amount'] = max_amount
        item_spec['name'] = name
        item_spec['type'] = type
        item_spec['location'] = location

        self.items.append(item_spec)


class ItemAdder(object):
    """
    Class for adding items
    """
    __logger_name__ = 'pyherc.generators.level.items.ItemAdder'

    @Logged(__logger_name__)
    def __init__(self, item_generator, configuration, rng):
        """
        Default constructor

        Args:
            item_generator: ItemGenerator instance
            configuration: ItemAdderConfiguration
            rng: random number generator
        """
        super(ItemAdder, self).__init__()
        self.item_generator = item_generator
        self.configuration = configuration
        self.rng = rng

    @Logged(__logger_name__)
    def __get_level_types(self):
        """
        Get level types this item adder can be used at
        """
        return self.configuration.level_types

    @Logged(__logger_name__)
    def add_items(self, level):
        """
        Add items

        Args:
            level: Level to add items
        """
        item_list = self.configuration.items
        items = []

        for item in item_list:
            items.extend(self.generate_items(item))

        self.place_items(items, level)

    @Logged(__logger_name__)
    def generate_items(self, item_spec):
        """
        Generate items according to specification

        Args:
            item_spec: Dictionary specifying items to create

        Returns
            tupple (item_spec, item)
            where item_spec is specification used to generate item
            and item is generated Item
        """
        items = []
        amount = self.rng.randint(item_spec['min_amount'],
                                  item_spec['max_amount'])

        params = {}
        if item_spec['name'] != None:
            params['name'] = item_spec['name']
        else:
            params['type'] = item_spec['type']

        for i in range(amount):
            new_item = self.item_generator.generate_item(params)
            items.append((item_spec, new_item))

        return items

    @Logged(__logger_name__)
    def place_items(self, items, level):
        """
        Place items to level

        Args:
            item: list of tupples (item_spec, item)
            level: level to place items
        """
        for item in items:
            location_type = item[0]['location']

            if location_type == None:
                location_type = 'any'

            locations = level.get_locations_by_type(location_type)

            location = self.rng.choice(locations)

            level.add_item(item[1], location)

    level_types = property(__get_level_types)

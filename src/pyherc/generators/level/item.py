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
Classes for item generation
"""
from pyherc.aspects import log_debug, log_info
from pyherc.data import (add_item, get_locations_by_tag, blocks_movement, 
                         get_trap, safe_passage)


class ItemAdder():
    """
    Class for adding items
    """
    @log_debug
    def __init__(self, item_generator, configuration, rng):
        """
        Default constructor

        :param item_generator: configured item generator
        :type item_generator: ItemGenerator
        :param configuration: configuration
        :type configuration: [{}]
        :param rng: random number generator
        :type rng: Random
        """
        super(ItemAdder, self).__init__()
        self.item_generator = item_generator
        self.configuration = configuration
        self.rng = rng

    @log_debug
    def __get_level_types(self):
        """
        Get level types this item adder can be used at
        """
        return self.configuration.level_types

    def __call__(self, level):
        """
        Add items
        """
        self.add_items(level)

    @log_info
    def add_items(self, level):
        """
        Add items

        :param level: level to add items
        :type level: Level
        """
        items = []

        for item in self.configuration:
            items.extend(self.generate_items(item))

        self.place_items(items, level)

    @log_info
    def generate_items(self, item_spec):
        """
        Generate items according to specification

        :param item_spec: Dictionary specifying items to create
        :type item_spec: dict
        :returns: tupple (item_spec, item)
        """
        items = []
        amount = self.rng.randint(item_spec['min_amount'],
                                  item_spec['max_amount'])

        for i in range(amount):
            new_item = self.item_generator.generate_item(
                name=item_spec['name'],
                item_type=item_spec['type'])
            items.append((item_spec, new_item))

        return items

    @log_info
    def place_items(self, items, level):
        """
        Place items to level

        :param items: list of tupples (item_spec, item)
        :param level: level to place items
        :type level: Level
        """
        for item in items:
            location_type = item[0]['location']

            if location_type is None:
                location_type = 'any'

            locations = [location for location in (get_locations_by_tag(level, location_type))
                         if safe_passage(level, location)]

            if locations:
                location = self.rng.choice(locations)
                add_item(level, location, item[1])


    level_types = property(__get_level_types)

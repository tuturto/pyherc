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
Classes for item generation
"""
from pyherc.aspects import log_debug, log_info
from pyherc.data import (add_item, get_locations_by_tag, blocks_movement, 
                         safe_passage)


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

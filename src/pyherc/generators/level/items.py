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
class ItemAdderConfiguration(object):
    """
    Configuration for ItemAdder
    """
    def __init__(self):
        """
        Default constructor
        """
        super(ItemAdderConfiguration, self).__init__()

    def add_item(self, min_amount, max_amount, name = None, type = None,
                 location = None):
        """
        Adds item to configuration

        Args:
            item: specification for item
        """
        pass


class ItemAdder(object):
    """
    Class for adding items
    """
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

    def add_items(self, level):
        """
        Add items

        Args:
            level: Level to add items
        """
        pass




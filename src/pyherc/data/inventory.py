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
Module for Inventory related classes
"""

from pyherc.aspects import log_debug


class Inventory():
    """
    Represents an inventory of items
    """
    @log_debug
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.__items = []

        self.ring = None
        self.weapon = None
        self.gloves = None
        self.boots = None
        self.belt = None
        self.helm = None
        self.necklace = None
        self.projectiles = None
        self.shield = None
        self.armour = None

    @log_debug
    def __len__(self):
        """
        Length of the container
        """
        return len(self.__items)

    @log_debug
    def __getitem__(self, key):
        """
        Access an item in Inventory
        """
        return self.__items.__getitem__(key)

    @log_debug
    def __setitem__(self, key, value):
        """
        Set item in inventory
        """
        self.__items.__setitem__(key, value)

    @log_debug
    def __delitem__(self, key):
        """
        Delete item from inventory
        """
        item = self.__items[key]
        self.remove(item)

    @log_debug
    def __iter__(self):
        """
        Get iterator for content of inventory
        """
        return self.__items.__iter__()

    @log_debug
    def append(self, item):
        """
        Append an item into inventory
        """
        self.__items.append(item)

    @log_debug
    def remove(self, item):
        """
        Remove item from inventory

        :param item: item to remove
        :type item: Item
        """
        self.__items.remove(item)

        if item == self.weapon:
            self.weapon = None
        if item == self.armour:
            self.armour = None
        if item == self.projectiles:
            self.projectiles = None
        if item == self.boots:
            self.boots = None

    def _repr_pretty_(self, p, cycle):
        """
        Pretty print for IPython

        :param p: printer to write
        :param cycle: has pretty print detected a cycle?
        """
        if cycle:
            p.text('Inventory(...)')
        else:
            p.text('Inventory:')
            for item in self.__items:
                p.pretty(item)
                p.breakable()

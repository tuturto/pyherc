#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Module for inventory screen
"""

from pyherc.aspects import logged

class InventoryScreen(object):
    """
    Class for displaying inventero screen

    .. versionaddedd:: 0.9
    """
    @logged
    def __init__(self, items, character, config, screen):
        """
        Default constructor
        """
        super(InventoryScreen, self).__init__()

        self.items = items
        self.character = character
        self.config = config
        self.screen = screen.subwin(20, 75, 2, 2)

        self.keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D']

    @logged
    def show(self):
        """
        Show inventory screen
        """
        self.screen.clear()
        self.screen.border()

        for index, item in enumerate(self.items):
            if index < 15:
                column = 1
                row = 1 + index
            else:
                column = 37
                row = 1 + index - 15

            self.screen.addstr(1 + index, 1,
                               '{0} {1}'.format(self.keys[index],
                                                item.get_name(self.character,
                                                              True)))

        self.screen.refresh()

        key = chr(self.screen.getch())
        if key in self.keys:
            index = self.keys.index(key)
            if index < len(self.items):
                return self.items[index]

        return None

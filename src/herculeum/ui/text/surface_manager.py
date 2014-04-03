# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
Module for handling loading of images and icons
"""
import curses

from pyherc.aspects import log_debug


class CursesSurfaceManager():
    """
    Class for managing glyphs

    .. versionadded:: 0.9
    """
    @log_debug
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.resourcesLoaded = 0
        self.icons = {}
        self.attributes = {}

    @log_debug
    def load_resources(self):
        """
        Load graphics from files
        """
        pass

    @log_debug
    def add_icon(self, key, filename, ascii_char, attributes = None):
        """
        Add icon to internal collection
        """
        if not (hasattr(key, 'upper') or hasattr(key, 'real')):
            key = key[0]

        if not key in self.icons:
            self.icons[key] = ascii_char

            if attributes == None:
                used_attributes = curses.A_NORMAL | self.get_attribute_by_name('white')
            else:
                used_attributes = curses.A_NORMAL
                for elem in attributes:
                    used_attributes = used_attributes | self.get_attribute_by_name(elem)

            self.attributes[key] = used_attributes

        return key

    def get_attribute_by_name(self, attribute_name):
        """
        Get attribute based on name
        """
        if attribute_name == 'blue':
            return curses.color_pair(1)
        elif attribute_name == 'cyan':
            return curses.color_pair(2)
        elif attribute_name == 'green':
            return curses.color_pair(3)
        elif attribute_name == 'magenta':
            return curses.color_pair(4)
        elif attribute_name == 'red':
            return curses.color_pair(5)
        elif attribute_name == 'white':
            return curses.color_pair(6)
        elif attribute_name == 'yellow':
            return curses.color_pair(7)
        elif attribute_name == 'bold':
            return curses.A_BOLD
        elif attribute_name == 'normal':
            return curses.A_NORMAL
        elif attribute_name == 'dim':
            return curses.A_DIM

    def get_attribute(self, id):
        """
        Get attriutes with ID
        """
        if id in self.attributes:
            return self.attributes[id]
        else:
            return curses.A_NORMAL | curses.color_pair(6)

    def get_icon(self, id):
        """
        Get icon with ID

        :param id: ID number of the icon to retrieve
        :type id: int
        :returns: icon if found, otherwise empty icon
        :rtype: string
        """
        if not id:
            return ' '

        if not (hasattr(id, 'upper') or hasattr(id, 'real')):
            id = id[0]

        if id in self.icons:
            return self.icons[id]
        else:
            return 'x'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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
Module containing classes to represent Portals
"""

import random
import logging
import pyherc.data.tiles
from pyherc.aspects import Logged

class Portal(object):
    """
    Portal linking two levels together
    """
    logged = Logged()

    @logged
    def __init__(self, icons, level_generator):
        """
        Default constructor

        Args:
            icons: (my_icon, icon for other end)
            level_generator: LevelGenerator for proxy portals
        """
        super(Portal, self).__init__()
        self.level = None
        self.location = ()
        self.__icons = icons
        self.__other_end = None
        self.level_generator = level_generator
        self.model = None
        self.logger = logging.getLogger('pyherc.data.dungeon.Portal')

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        properties = dict(self.__dict__)
        del properties['logger']
        return properties

    def __setstate__(self, properties):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(properties)
        self.logger = logging.getLogger('pyherc.data.dungeon.Portal')

    @logged
    def __get_other_end(self):
        """
        Returns the other end of the portal
        """
        if self.__other_end == None and self.level_generator != None:
            self.level_generator.generate_level(self)

        return self.__other_end

    @logged
    def __set_other_end(self, portal):
        """
        Set the other end of the portal

        Args:
            portal: portal where this one leads
        """
        self.__other_end = portal

    def __get_icon(self):
        """
        Get icon to display this portal
        """
        return self.__icons[0]

    def __set_icon(self, icon):
        """
        Set icon to display this portal
        """
        if self.__icons == None:
            self.__icons = (None, None)
        self.__icons = (icon, self.__icons[1])

    def __get_other_end_icon(self):
        """
        Get icon used for other end of this portal
        """
        return self.__icons[1]

    other_end = property(__get_other_end, __set_other_end)
    icon = property(__get_icon, __set_icon)
    other_end_icon = property(__get_other_end_icon)

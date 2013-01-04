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
Module for handling loading of images and icons
"""
from pyherc.aspects import logged

class CursesSurfaceManager(object):
    """
    Class for managing glyphs

    .. versionadded:: 0.9
    """
    @logged
    def __init__(self):
        """
        Default constructor
        """
        super(CursesSurfaceManager, self).__init__()
        self.resourcesLoaded = 0
        self.icons = {}

    @logged
    def load_resources(self):
        """
        Load graphics from files
        """
        pass

    @logged
    def add_icon(self, key, filename, ascii_char):
        """
        Add icon to internal collection
        """
        self.icons[key] = ascii_char

        return key

    @logged
    def get_icon(self, id):
        """
        Get icon with ID

        :param id: ID number of the icon to retrieve
        :type id: int
        :returns: icon if found, otherwise empty icon
        :rtype: string
        """
        if id in self.icons:
            return self.icons[id]
        else:
            return 'X'

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
    """
    @logged
    def __init__(self):
        """
        Default constructor
        """
        super(CursesSurfaceManager, self).__init__()
        self.resourcesLoaded = 0

    @logged
    def load_resources(self):
        """
        Load graphics from files
        """
        pass

    @logged
    def add_icon(self, key, filename):
        """
        Add icon to internal collection
        """
        pass

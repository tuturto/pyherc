#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module for herculeum main configuration
"""
import pyherc.config
from herculeum.gui.surfaceManager import SurfaceManager

class Configuration(pyherc.config.Configuration):

    def __init__(self, base_path, model):
        """
        Default constructor
        """
        super(Configuration, self).__init__(base_path, model)

        self.surface_manager = None

    def initialise(self, level_config):
        super(Configuration, self).initialise(level_config)

        self.resolution = (800, 600)
        self.full_screen = True
        self.caption = 'Herculeum'

        self.surface_manager = SurfaceManager()
        self.surface_manager.load_resources(self.base_path)

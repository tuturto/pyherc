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
Module for herculeum main configuration
"""
import pyherc.config
from herculeum.gui.surfaceManager import SurfaceManager
from PyQt4.QtCore import Qt

class Configuration(pyherc.config.Configuration):
    """
    Configuration for herculeum
    """

    def __init__(self, base_path, model, config_package):
        """
        Default constructor

        :param base_path: path to resources
        :type base_path: string
        :param model: model to use in configuration
        :param type: Model
        """
        super(Configuration, self).__init__(base_path, model)

        self.surface_manager = SurfaceManager(base_path)
        self.surface_manager.load_resources(base_path)

        self.context = ConfigurationContext(config_package,
                                            base_path,
                                            self.surface_manager)

        self.controls = ControlsConfiguration()

    def initialise(self):
        """
        Initialise configuration
        """
        super(Configuration, self).initialise(self.context)

class ConfigurationContext(object):
    """
    Class to relay information between different configuration phases

    .. versionadded:: 0.6
    """
    def __init__(self, config_package, base_path, surface_manager):
        """
        Default constructor

        :param config_package: package containing configurations
        :type config_package: Package
        :param base_path: location of resource files
        :type base_path: string
        :param surface_manager: manager to handle graphics
        :type surface_manager: SurfaceManager
        """
        super(ConfigurationContext, self).__init__()
        self.config_package = config_package
        self.base_path = base_path
        self.surface_manager = surface_manager

class ControlsConfiguration(object):
    """
    Configuration for user interface controls

    .. versionadded:: 0.8
    """
    def __init__(self):
        """
        Default constructor
        """
        super(ControlsConfiguration, self).__init__()

        self.move_left = [Qt.Key_4, Qt.Key_Left, Qt.Key_H]
        self.move_up_left = [Qt.Key_7, Qt.Key_Y]
        self.move_up = [Qt.Key_8, Qt.Key_Up, Qt.Key_K]
        self.move_up_right = [Qt.Key_9, Qt.Key_U]
        self.move_right = [Qt.Key_6, Qt.Key_Right, Qt.Key_L]
        self.move_down_right = [Qt.Key_3, Qt.Key_N]
        self.move_down = [Qt.Key_2, Qt.Key_Down, Qt.Key_J]
        self.move_down_left = [Qt.Key_1, Qt.Key_B]

        self.action_a = [Qt.Key_Space, Qt.Key_Z, Qt.Key_5]
        self.action_b = [Qt.Key_Control, Qt.Key_X]
        self.action_x = [Qt.Key_Alt]
        self.action_y = [Qt.Key_Tab]

        self.start = [Qt.Key_Return]
        self.back = [Qt.Key_Escape]

        self.left_shoulder = [Qt.Key_Insert, Qt.Key_PageUp, Qt.Key_Q]
        self.right_shoulder = [Qt.Key_Delete, Qt.Key_PageDown, Qt.Key_W]

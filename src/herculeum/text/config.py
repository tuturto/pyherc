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
Module for UI Configuration
"""

class CursesControlsConfiguration(object):
    """
    Configuration for user interface controls

    .. versionadded:: 0.9
    """
    def __init__(self):
        """
        Default constructor
        """
        super(CursesControlsConfiguration, self).__init__()

        self.move_left = ['4']
        self.move_up_left = ['7']
        self.move_up = ['8']
        self.move_up_right = ['9']
        self.move_right = ['6']
        self.move_down_right = ['3']
        self.move_down = ['2']
        self.move_down_left = ['1']

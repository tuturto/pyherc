#!/usr/bin/env python3
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
Module for UI Configuration
"""
import curses


class CursesControlsConfiguration():
    """
    Configuration for user interface controls

    .. versionadded:: 0.9
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.move_left = ['4']
        self.move_up = ['8']
        self.move_right = ['6']
        self.move_down = ['2']

        self.action_a = ['5']
        self.back = [' ']

        self.colours = {}

        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK);
            curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK);
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK);
            curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK);
            curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK);
            curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK);
            curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK);

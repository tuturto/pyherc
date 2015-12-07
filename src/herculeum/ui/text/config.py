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

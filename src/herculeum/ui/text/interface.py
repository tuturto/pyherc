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
Module for curses user interface
"""
import curses

from herculeum.ui.controllers import StartGameController
from herculeum.ui.text.main_window import MainWindow


class CursesUserInterface():
    """
    Class for curses user interface

    .. versionadded:: 0.9
    """
    def __init__(self, application):
        """
        Default constructor
        """
        super().__init__()

        self.application = application
        self.splash_screen = None

        self.curses = curses.initscr()

        if curses.has_colors():
            curses.start_color()

        self.screen = self.curses.subwin(24, 80, 0, 0)

        self.screen.refresh()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

    def show_splash_screen(self):
        """
        Show splash screen
        """
        pass

    def show_main_window(self):
        """
        Show main window
        """
        main_window = MainWindow(self.application,
                                 self.application.surface_manager,
                                 self.screen,
                                 StartGameController(self.application.level_generator_factory,
                                                     self.application.creature_generator,
                                                     self.application.item_generator,
                                                     self.application.config.start_level))

        main_window.show_new_game()
        main_window.show_map_window()

        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()

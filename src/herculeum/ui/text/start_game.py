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
Module for start game related functionality
"""
class StartGameScreen():
    """
    Screen to start game

    .. versionadded:: 0.9
    """
    def __init__(self, generator, application, screen):
        """
        Default constructor
        """
        super().__init__()

        self.generator = generator
        self.class_names = self.generator.configuration.keys()
        self.screen = screen


    def show(self):
        """
        Show this screen
        """
        self.draw_screen()

        selection = None

        while selection is None:
            selection = self.screen.getch()

            try:
                selection = int(chr(selection))
            except ValueError:
                selection = None

            if selection < 0 or selection > len(self.class_names) - 1:
                selection = None

        for index, class_name in enumerate(self.class_names):
            if index == selection:
                return self.generator.generate_creature(class_name)

    def draw_screen(self):
        """
        Draw screen
        """
        self.screen.clear()
        for index, class_name in enumerate(self.class_names):
            self.screen.addstr(5 + index, 20,
                               '{0}. {1}'.format(index, class_name))
        self.screen.refresh()

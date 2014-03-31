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

        while selection == None:
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

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
Module for character screen
"""
class CharacterScreen():
    """
    Character screen

    .. versionadded:: 0.9
    """
    def __init__(self, character, screen):
        """
        Default constructor
        """
        super(CharacterScreen, self).__init__()

        self.screen = screen.subwin(20, 75, 2, 2)
        self.character = character

    def show(self):
        """
        Show the dialog
        """
        self._draw_screen()
        chr(self.screen.getch())

    def _draw_screen(self):
        """
        Update the screen
        """
        self.screen.clear()
        self.screen.border()

        player = self.character

        self.screen.addstr(1, 1, 'hp: {0}/{1}'.format(player.hit_points,
                                                     player.max_hp))
        self.screen.addstr(2, 1, 'mana: 0/0')
        self.screen.addstr(1, 37, 'body: {0}'.format(player.body))
        self.screen.addstr(2, 37, 'mind: {0}'.format(player.mind))
        self.screen.addstr(3, 37, 'finesse: {0}'.format(player.finesse))

        self.screen.addstr(5, 1, 'Effects:')
        self.screen.addstr(5, 37, 'Skills:')
        for index, effect in enumerate(player.get_effects()):
            self.screen.addstr(6 + index, 1, effect.title)

        self.screen.refresh()

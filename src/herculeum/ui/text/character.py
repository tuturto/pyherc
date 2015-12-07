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

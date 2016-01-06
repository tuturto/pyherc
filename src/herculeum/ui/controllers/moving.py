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
Module for moving
"""
from pyherc.ports import is_move_legal, move, attack
from pyherc.data import get_character


class MoveController():
    """
    Controller for moving around

    .. versionadded:: 0.9
    """
    def __init__(self, action_factory, rng):
        """
        Default constructor
        """
        super().__init__()

        self.action_factory = action_factory # TODO: not needed anymore
        self.rng = rng

    def move_or_attack(self, character, direction):
        """
        Move or attack
        """
        level = character.level

        if is_move_legal(character,
                         direction):
            move(character, direction)
        elif direction != 9:
            loc = character.get_location_at_direction(direction)
            if get_character(level, loc) is not None:
                attack(character,
                       direction,
                       self.rng)

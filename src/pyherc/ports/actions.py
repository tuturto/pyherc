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
Port to issue actions
"""
from pyherc.rules import is_move_legal, move


class ActionsPort():
    """
    Port to issue actions with

    .. versionadded:: 0.10
    """

    def __init__(self, action_factory):
        """
        Default constructor

        :param action_factory: action factory to use
        :type action_factory: ActionFactory
        """
        super().__init__()

        self.action_factory = action_factory

    def move_character(self, character, direction):
        """
        Move a character to given direction

        :param character: character to move
        :type character: Character
        :param direction: direction to move to
        :type direction: int (1-8)
        """
        move(character=character,
             direction=direction,
             action_factory=self.action_factory)

    def is_move_legal(self, character, direction):
        """
        Check if character is allowed to move to given direction

        :param character: character to move
        :type character: Character
        :param direction: direction to move to
        :type direction: int (1-8)
        """
        return is_move_legal(character=character,
                             direction=direction,
                             movement_mode='walk',
                             action_factory=self.action_factory)

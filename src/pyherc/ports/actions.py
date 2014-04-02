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

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
Module for moving
"""
from pyherc.rules import attack, is_move_legal, move
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

        self.action_factory = action_factory
        self.rng = rng

    def move_or_attack(self, character, direction, movement_mode):
        """
        Move or attack
        """
        level = character.level

        if is_move_legal(character,
                         direction,
                         movement_mode,
                         self.action_factory):
            move(character, direction, self.action_factory)
        elif direction != 9:
            loc = character.get_location_at_direction(direction)
            if get_character(level, loc) is not None:
                attack(character,
                       direction,
                       self.action_factory,
                       self.rng)

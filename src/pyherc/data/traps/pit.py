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

# flake8: noqa

"""
Package for traps
"""
from pyherc.data.new_character import set_hit_points

class PitTrap():
    """
    Trap to fall in

    .. versionadded:: 0.11
    """
    def __init__(self):
        """
        Default constructor
        """
        self.location = ( )

    def on_enter(self, character):
        """
        Called when a character enter the trap

        :param character: character who just stepped on the trap
        :type character: Character
        """
        set_hit_points(character, -1)

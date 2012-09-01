#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module for checking end conditions
"""

from pyherc.events import DeathEvent
from pyherc.aspects import Logged

class Dying(object):
    """
    Rules for actions happening when dying

    .. versionadded:: 0.6
    """
    logged = Logged()

    @logged
    def __init__(self):
        """
        Default constructor
        """
        super(Dying, self).__init__()

    @logged
    def check_dying(self, character):
        """
        Check if character dies and process it
        """
        if character.hit_points <= 0:
            for item in character.inventory:
                #drop items
                pass

            character.raise_event(DeathEvent(deceased = character,
                                             affected_tiles = character.location))
            character.level.remove_creature(character)

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
Module for checking end conditions
"""

from pyherc.aspects import log_debug, log_info
from pyherc.data.model import DIED_IN_DUNGEON, ESCAPED_DUNGEON
from pyherc.events import DeathEvent, DropEvent
from pyherc.data import remove_character, add_item


class Dying():
    """
    Rules for actions happening when dying

    .. versionadded:: 0.6
    """
    @log_debug
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    @log_debug
    def check_dying(self, character):
        """
        Check if character dies and process it
        """
        if not character.level:
            return

        if character.hit_points <= 0:
            for item in character.inventory:
                character.inventory.remove(item)
                add_item(character.level, character.location, item)
                character.raise_event(DropEvent(character,
                                                item))

            if character.inventory.weapon is not None:
                add_item(character.level,
                         character.location,
                         character.inventory.weapon)
                character.raise_event(DropEvent(character,
                                                item))
                character.inventory.weapon = None

            if character == character.model.player:
                character.model.end_condition = DIED_IN_DUNGEON

            character.raise_event(
                DeathEvent(deceased=character,
                           affected_tiles=character.location))
            remove_character(character.level, character)

    @log_info
    def calculate_score(self, character):
        """
        Calculate score for character

        .. versionadded:: 0.8
        """
        end_condition = character.model.end_condition

        score = sum((item.cost for item in character.inventory))

        if end_condition == DIED_IN_DUNGEON:
            score = int(score * 0.75)
        elif end_condition == ESCAPED_DUNGEON:
            score = int(score * 1.25)

        return score

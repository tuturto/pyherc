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
Module for checking end conditions
"""

from pyherc.aspects import log_debug, log_info
from pyherc.data.model import DIED_IN_DUNGEON, ESCAPED_DUNGEON
from pyherc.events import new_death_event, new_drop_event
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
                character.raise_event(new_drop_event(character,
                                                     item))

            if character.inventory.weapon is not None:
                add_item(character.level,
                         character.location,
                         character.inventory.weapon)
                character.raise_event(new_drop_event(character,
                                                     item))
                character.inventory.weapon = None

            if character == character.model.player:
                character.model.end_condition = DIED_IN_DUNGEON

            character.raise_event(
                new_death_event(deceased=character))
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

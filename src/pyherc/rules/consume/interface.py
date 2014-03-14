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
Public interface for consuming actions
"""

from pyherc.aspects import log_debug, log_info
from pyherc.rules.public import ActionParameters


@log_info
def drink(character, potion, action_factory):
    """
    Drink potion

    :param character: character about to drink
    :type character: Character
    :param potion: potion to drink
    :type potion: Item
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory
    """
    action = action_factory.get_action(DrinkParameters(character,
                                                       potion))
    action.execute()


class DrinkParameters(ActionParameters):
    """
    Object for controlling drink action creation
    """
    @log_debug
    def __init__(self, character, item):
        """
        Construct drink parameters

        Args:
            character: Character moving
            item: Item to drink
        """
        super().__init__()

        self.action_type = 'drink'
        self.character = character
        self.item = item
        self.model = None

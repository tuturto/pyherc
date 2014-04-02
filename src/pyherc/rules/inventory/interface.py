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
Public interface for inventory rules package
"""

from pyherc.aspects import log_debug, log_info
from pyherc.rules.public import ActionParameters


@log_info
def pick_up(character, item, action_factory):
    """
    Pick up item

    :param character: character picking up the item
    :type character: Character
    :param item: item to pick up
    :type item: Item
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory

    .. versionadded:: 0.4
    """
    action = action_factory.get_action(InventoryParameters(character,
                                                           item,
                                                           'pick up'))
    action.execute()


@log_info
def drop_item(character, item, action_factory):
    """
    Drop item from inventory

    :param character: character dropping the item
    :type character: Character
    :param item: item to drop
    :type item: Item
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory

    .. versionadded:: 0.5
    """
    action = action_factory.get_action(InventoryParameters(character,
                                                           item,
                                                           'drop'))
    action.execute()


@log_info
def equip(character, item, action_factory):
    """
    Wear item from inventory

    :param character: character equipping the item
    :type character: Character
    :param item: item to equip
    :type item: Item
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory

    .. versionadded:: 0.8
    """
    action = action_factory.get_action(InventoryParameters(character,
                                                           item,
                                                           'equip'))
    action.execute()


@log_info
def unequip(character, item, action_factory):
    """
    Unequip item

    :param character: character unequipping the item
    :type character: Character
    :param item: item to unequip
    :type item: Item
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory

    .. versionadded:: 0.8
    """
    action = action_factory.get_action(InventoryParameters(character,
                                                           item,
                                                           'unequip'))
    action.execute()


class InventoryParameters(ActionParameters):
    """
    Class for controlling inventory action creation
    """
    @log_debug
    def __init__(self, character, item, sub_action):
        """
        Construct inventory parameters

        :param character: character manipulating the item
        :type character: Character
        :param item: item to manipulate
        :type item: Item
        :param sub_action: type of action to perform
        :type sub_action: string
        """
        super().__init__()

        self.action_type = 'inventory'
        self.sub_action = sub_action
        self.character = character
        self.item = item

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

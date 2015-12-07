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
Module defining classes related to inventory actions
"""
from pyherc.data import is_armour, is_weapon, is_ammunition, is_boots
from pyherc.aspects import log_debug, log_info
from pyherc.events import new_equip_event
from pyherc.rules.factory import SubActionFactory


class EquipFactory(SubActionFactory):
    """
    Factory for creating equip actions

    .. versionadded:: 0.8
    """
    @log_debug
    def __init__(self):
        """
        Constructor for this factory
        """
        super().__init__()
        self.sub_action = 'equip'

    @log_debug
    def can_handle(self, parameters):
        """
        Can this factory process these parameters

        :param parameters: parameters to check
        :returns: True if factory is capable of handling parameters
        :rtype: Boolean
        """
        return self.sub_action == parameters.sub_action

    @log_info
    def get_action(self, parameters):
        """
        Create an equip action

        :param parameters: parameters used to control creation
        :type parameters: InventoryParameters
        """
        return EquipAction(parameters.character, parameters.item)


class EquipAction():
    """
    Action for equiping an item

    .. versionadded:: 0.8
    """
    @log_debug
    def __init__(self, character, item):
        """
        Default constructor

        :param character: character wearing the item
        :type character: Character
        :param item: item to equip
        :type item: Item
        """
        super().__init__()

        self.character = character
        self.item = item

    @log_info
    def execute(self):
        """
        Executes this action
        """
        if is_armour(self.item):
            self.character.inventory.armour = self.item
            self.character.raise_event(new_equip_event(self.character,
                                                       self.item))
        if is_weapon(self.item):
            self.character.inventory.weapon = self.item
            self.character.raise_event(new_equip_event(self.character,
                                                       self.item))
        if is_ammunition(self.item):
            self.character.inventory.projectiles = self.item
            self.character.raise_event(new_equip_event(self.character,
                                                       self.item))
        elif is_boots(self.item):
            self.character.inventory.boots = self.item
            self.character.raise_event(new_equip_event(self.character,
                                                       self.item))

    @log_debug
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if move is possible, false otherwise
        :rtype: Boolean
        """
        return True

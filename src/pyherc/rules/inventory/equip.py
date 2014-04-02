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
Module defining classes related to inventory actions
"""
from pyherc.aspects import log_debug, log_info
from pyherc.events import EquipEvent
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
        if self.item.get_main_type() == 'armour':
            self.character.inventory.armour = self.item
            self.character.raise_event(EquipEvent(self.character,
                                                  self.item))
        elif self.item.get_main_type() == 'weapon':
            self.character.inventory.weapon = self.item
            self.character.raise_event(EquipEvent(self.character,
                                                  self.item))
        elif self.item.get_main_type() == 'ammunition':
            self.character.inventory.projectiles = self.item
            self.character.raise_event(EquipEvent(self.character,
                                                  self.item))

    @log_debug
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if move is possible, false otherwise
        :rtype: Boolean
        """
        return True

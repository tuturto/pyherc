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
Inventory manipulation related factories are defined here
"""
from pyherc.aspects import log_debug, log_info
from pyherc.rules.factory import SubActionFactory
from pyherc.rules.inventory.action import DropAction, PickUpAction


class PickUpFactory(SubActionFactory):
    """
    Factory for creating pick up actions

    .. versionadded:: 0.4
    """
    @log_debug
    def __init__(self):
        """
        Constructor for this factory
        """
        super().__init__()
        self.sub_action = 'pick up'

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
        Create a pick up action

        :param parameters: parameters used to control creation
        :type parameters: InventoryParameters
        """
        return PickUpAction(parameters.character, parameters.item)


class DropFactory(SubActionFactory):
    """
    Factory for creating drop actions

    .. versionadded:: 0.5
    """
    @log_debug
    def __init__(self):
        """
        Constructor for this factory
        """
        super().__init__()
        self.sub_action = 'drop'

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
        Create a drop action

        :param parameters: parameters used to control creation
        :type parameters: InventoryParameters
        """
        return DropAction(parameters.character, parameters.item)


class InventoryFactory(SubActionFactory):
    """
    Factory for constructing inventory actions

    .. versionadded:: 0.4
    """
    @log_debug
    def __init__(self, factories):
        """
        Constructor for this factory

        :param factories: a single Factory or list of Factories to use
        :type factories: SubActionFactory or [SubActionFactory]
        """
        super().__init__()
        self.action_type = 'inventory'

        if hasattr(factories, '__iter__'):
            self.factories = factories
        else:
            self.factories = []
            self.factories.append(factories)

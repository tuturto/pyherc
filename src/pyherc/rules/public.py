# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Public interface for action subsystem

Classes:
ActionFactory - Class used to contruct Action objects
ActionParameters - Class used to guide Action construction

AttackParameters - Class used to guide contruction of attack related actions
DrinkParameters - Class used to guide drinking related actions
InventoryParameters - Class used to guide inventory related actions
SpellCastingParameteres - Class used to guide spell casting
"""

from pyherc.aspects import log_debug, log_info

class ActionFactory():
    """
    Object for creating actions
    """

    @log_debug
    def __init__(self, model, factories):
        """
        Construct ActionFactory

        Args:
            model: model to register for the factory
            factories: a single Factory or list of Factories to use
        """
        if hasattr(factories, '__iter__'):
            self.factories = factories
        else:
            self.factories = []
            self.factories.append(factories)

        self.model = model

    @log_info
    def get_action(self, parameters):
        """
        Create an action

        Args:
            parameters: Parameters used to control action creation
        """
        factory = self.get_sub_factory(parameters)
        assert factory != None, 'suitable factory not configured'
        return factory.get_action(parameters)

    @log_debug
    def get_sub_factories(self):
        """
        Get all sub factories

        Returns:
            List of sub factories
        """
        return self.factories

    @log_debug
    def get_sub_factory(self, parameters):
        """
        Get sub factory to handle parameters

        Args:
            parameters: Parameters to use for searching the factory

        Returns:
            Sub factory if found, None otherwise
        """
        subs = [x for x in self.factories if x.can_handle(parameters)]

        if len(subs) == 1:
            return subs[0]
        else:
            return None

class ActionParameters():
    """
    Object for controlling action creation
    """

    @log_debug
    def __init__(self):
        """
        Default constructor
        """
        self.action_type = 'default'

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
        ActionParameters.__init__(self)

        self.action_type = 'drink'
        self.character = character
        self.item = item
        self.model = None

    @log_debug
    def __str__(self):
        """
        Get string representation of this object
        """
        return 'drink parameters'

class WaitParameters(ActionParameters):
    """
    Class for controlling waiting

    .. versionadded:: 0.10
    """
    @log_debug
    def __init__(self, character, time_to_wait):
        """
        Construct wait parameters

        :param character: character to wait
        :type character: Character
        :param time_to_wait: amount of ticks to wait
        :type time_to_wait: int
        """
        super().__init__()

        self.action_type = 'wait'
        self.character = character
        self.time_to_wait = time_to_wait

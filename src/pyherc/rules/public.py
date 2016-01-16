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
Public interface for action subsystem

Classes:
ActionFactory - Class used to contruct Action objects
ActionParameters - Class used to guide Action construction

AttackParameters - Class used to guide contruction of attack related actions
DrinkParameters - Class used to guide drinking related actions
InventoryParameters - Class used to guide inventory related actions
SpellCastingParameteres - Class used to guide spell casting
"""

from hymn.types.maybe import Just, Nothing, is_nothing
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
        super().__init__()

        if hasattr(factories, '__iter__'):
            self.factories = factories
        else:
            self.factories = []
            self.factories.append(factories)

        self.model = model

    def __call__(self, parameters):
        """
        Temporary magic method to make this behave like a function

        returns:
            Just(Action) when creation of Action was possible
            Nothing when creation of Action was not possible
        """
        iterator = iter(self.factories)
        res = Nothing
        for fn in iter(self.factories):
            res = fn(parameters)
            if not is_nothing(res):
                return res
        return Nothing

    @log_info
    def get_action(self, parameters):
        """
        Create an action

        Args:
            parameters: Parameters used to control action creation
        """
        factory = self.get_sub_factory(parameters)
        assert factory is not None, 'suitable factory not configured'
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

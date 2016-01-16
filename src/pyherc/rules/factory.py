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
Factory related classes are defined here
"""
import logging
from hymn.types.maybe import Nothing, Just

class SubActionFactory():
    """
    Factory to handle concrete creation of actions
    """
    def __init__(self, effect_factory=None):
        """
        Constructor for this factory

        Args:
            effect_factory: Initialised EffectsFactory
        """
        super().__init__()
        self.action_type = 'default'
        self.logger = logging.getLogger('pyherc.rules.factory.SubActionFactory')  # noqa
        self.factories = []
        self.effect_factory = effect_factory

    def __call__(self, parameters):
        """
        Temporary magic method to treat this factory as a function

        Returns:
            Just(Action) if factory is capable for creating required Action
            Nothing if factory can not create required Action
        """
        if self.can_handle(parameters):
            return Just(self.get_action(parameters))
        else:
            return Nothing        

    def get_sub_factory(self, parameters):
        """
        Get sub factory to handle parameters

        Args:
            parameters: Parameters to use for searching the factory
        """
        subs = [x for x in self.factories if x.can_handle(parameters)]

        if len(subs) == 1:
            return subs[0]
        else:
            return None

    def can_handle(self, parameters):
        """
        Can this factory process these parameters

        Args:
            parameters: Parameters to check

        Returns:
            True if factory is capable of handling parameters
        """
        return self.action_type == parameters.action_type

    def get_action(self, parameters):
        """
        Create an action

        Args:
            parameters: Parameters used to control action creation
        """
        sub = self.get_sub_factory(parameters)
        return sub.get_action(parameters)

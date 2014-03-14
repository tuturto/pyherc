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
Factory related classes are defined here
"""
import logging


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

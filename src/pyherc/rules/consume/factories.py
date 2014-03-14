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
Drinking and eating related factories are defined here
"""
from pyherc.rules.consume.action import DrinkAction
from pyherc.rules.factory import SubActionFactory


class DrinkFactory(SubActionFactory):
    """
    Factory for creating drink actions
    """
    def __init__(self, effect_factory, dying_rules):
        """
        Constructor for this factory
        """
        super().__init__(effect_factory)
        self.action_type = 'drink'
        self.dying_rules = dying_rules

    def get_action(self, parameters):
        """
        Create a drink action

        Args:
            parameters: Parameters used to control drink action creation
        """
        return DrinkAction(parameters.character,
                           parameters.item,
                           self.effect_factory,
                           self.dying_rules)

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
Module defining rules engine
"""


class RulesEngine():
    """
    Engine for rules of the game

    .. versionadded:: 0.6
    """
    def __init__(self, action_factory, dying_rules):
        """
        Default constructor

        :param action_factory: factory for actions
        :type action_factory: ActionFactory
        :param dying: rules for dying
        :type dying: Dying
        """
        super().__init__()

        self.__action_factory = action_factory
        self.__dying_rules = dying_rules

    def __get_action_factory(self):
        """
        Action factory of the rules engine
        """
        return self.__action_factory

    def __get_dying_rules(self):
        """
        Rules for dying
        """
        return self.__dying_rules

    action_factory = property(__get_action_factory)
    dying_rules = property(__get_dying_rules)

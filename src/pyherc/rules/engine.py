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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module for rules engine builder
"""
from pyherc.rules import RulesEngine
from mockito import mock

class RulesEngineBuilder(object):
    """
    Class to build rules engines
    """
    def __init__(self):
        """
        Default constructor
        """
        super(RulesEngineBuilder, self).__init__()

        self.action_factory = mock()
        self.dying_rules = mock()

    def build(self):
        """
        Builds rules engine
        """
        return RulesEngine(action_factory = self.action_factory,
                           dying_rules = self.dying_rules)
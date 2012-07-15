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
Tests for creature generation
"""
#pylint: disable=W0614
from pyherc.generators import NewCreatureGenerator as CreatureGenerator
from pyherc.test.matchers import has_effect_handle
from hamcrest import * #pylint: disable=W0401

from pyherc.generators import CreatureConfigurations
from pyherc.generators import CreatureConfiguration
from pyherc.rules.effects import EffectHandle
from random import Random

class TestCreatureGeneration(object):
    """
    Tests for creature generator
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestCreatureGeneration, self).__init__()
        self.creature_config = None
        self.generator = None

    def setup(self):
        """
        Setup test case
        """
        self.creature_config = CreatureConfigurations(Random())

        self.generator = CreatureGenerator(self.item_config)


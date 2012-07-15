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
from mockito import mock

from pyherc.generators import CreatureConfigurations
from pyherc.generators import CreatureConfiguration
from pyherc.rules.effects import EffectHandle
from pyherc.ai import FlockingHerbivore
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

        self.model = None
        self.action_factory = None
        self.rng = None

    def setup(self):
        """
        Setup test case
        """
        self.creature_config = CreatureConfigurations(Random())

        self.model = mock()
        self.action_factory = mock()
        self.rng = Random()

        self.creature_config.add_creature(
                        CreatureConfiguration(name = 'rat',
                                              body = 4,
                                              finesse = 12,
                                              mind = 2,
                                              hp = 2,
                                              speed = 2,
                                              icons = [100, 101],
                                              attack = 2,
                                              ai = FlockingHerbivore))

        self.creature_config.add_creature(
                        CreatureConfiguration(name = 'spider',
                                              body = 6,
                                              finesse = 12,
                                              mind = 8,
                                              hp = 6,
                                              speed = 1,
                                              icons = [102],
                                              attack = 4,
                                              ai = FlockingHerbivore,
                                              effect_handles = [EffectHandle(
                                                    trigger = 'on attack hit',
                                                    effect = 'minor poison',
                                                    parameters = None,
                                                    charges = 100)]))

        self.generator = CreatureGenerator(configuration = self.creature_config,
                                           model = self.model,
                                           action_factory = self.action_factory,
                                           rng = self.rng
                                           )

    def test_creating_simple_creature(self):
        """
        Test that simple creature can be created by name
        """
        creature = self.generator.generate_creature(name = 'rat')

        assert_that(creature.name, is_(equal_to('rat')))

    def test_creating_creature_with_effect(self):
        """
        Test that creature with effect can be created
        """
        creature = self.generator.generate_creature(name = 'spider')

        assert_that(creature, has_effect_handle())

    def test_creating_creature_with_ai(self):
        """
        Test that creature can have AI created
        """
        creature = self.generator.generate_creature(name = 'rat')

        assert_that(creature.artificial_intelligence,
                    is_(not_none()))

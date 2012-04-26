#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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
Module for testing time related functions
"""
#pylint: disable=W0614
import pyherc
import pyherc.rules.time
from pyherc.data.model import Model
from pyherc.data.model import Character
from pyherc.data.dungeon import Dungeon
from pyherc.data.dungeon import Level
from pyherc.rules.effects import Effect

from hamcrest import * #pylint: disable=W0401
from mockito import mock, verify, when, any

class TestTime:
    """
    Time related tests
    """

    def __init__(self):
        """
        Default constructor
        """
        self.creature1 = None
        self.creature2 = None
        self.creature3 = None
        self.model = None

    def setup(self):
        """
        Setup the test case
        """
        model = mock()
        action_factory = mock()
        rng = mock()

        self.creature1 = Character(model, action_factory, rng)
        self.creature2 = Character(model, action_factory, rng)
        self.creature3 = Character(model, action_factory, rng)

        self.model = Model()
        self.model.dungeon = Dungeon()
        self.model.dungeon.levels = Level((20, 20), 0, 0)

        self.creature1.tick = 5
        self.creature1.speed = 1
        self.creature1.name = 'creature 1'
        self.creature2.tick = 0
        self.creature2.speed = 2
        self.creature2.name = 'creature 2'
        self.creature3.tick = 3
        self.creature3.speed = 0.5
        self.creature3.name = 'creature 3'

        self.model.dungeon.levels.add_creature(self.creature1)
        self.model.dungeon.levels.add_creature(self.creature2)
        self.model.player = self.creature3
        self.model.dungeon.levels.add_creature(self.creature3)

    def test_get_next_zero_tick(self):
        """
        Test that system can tell whose turn it is to act
        One creature has tick of 0
        """
        creature = pyherc.rules.time.get_next_creature(self.model)
        assert_that(creature, is_(equal_to(self.creature2)))

    def test_get_next_positive_tick(self):
        """
        Test that system can tell whose turn it is to act
        All creatures have positive tick
        """
        self.creature1.tick = 5
        self.creature2.tick = 10
        self.creature3.tick = 3
        creature = pyherc.rules.time.get_next_creature(self.model)
        assert_that(creature, is_(equal_to(self.creature3)))

class TestEffectsAndTime:
    """
    Tests for effects and time
    """

    def __init__(self):
        """
        Default constructor
        """
        self.effect = None
        self.creature = None
        self.model = None
        self.level = None

    def setup(self):
        """
        Setup the test case
        """
        self.creature = mock(Character)
        self.creature.tick = 5
        self.model = mock(Model)
        self.model.player = self.creature
        self.level = mock(Level)
        self.level.creatures = [self.creature]
        self.creature.level = self.level

    def test_trigger_effect_on_time(self):
        """
        Test that effect will be triggered
        """
        effect = mock(Effect)
        effect.duration = 50
        effect.frequency = 5
        effect.tick = 5
        self.creature.active_effects = [effect]

        next_creature = pyherc.rules.time.get_next_creature(self.model)

        verify(effect).trigger()

    def test_tick_will_be_reset(self):
        """
        Test that tick of effect will be reset after it has been triggered
        """
        effect = Effect(duration = 50,
                        frequency = 5,
                        tick = 5)
        self.creature.active_effects = [effect]

        next_creature = pyherc.rules.time.get_next_creature(self.model)
        effect = self.creature.active_effects[0]

        assert_that(effect.tick, is_(equal_to(5)))

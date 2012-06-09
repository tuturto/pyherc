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
Module for testing time related functions
"""
#pylint: disable=W0614
import pyherc
from pyherc.data.model import Model
from pyherc.data import Dungeon
from pyherc.data import Level
from pyherc.rules.effects import Effect

from pyherc.test.builders import CharacterBuilder

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

        self.creature1 = (CharacterBuilder()
                            .with_tick(5)
                            .with_speed(1)
                            .with_name('creature 1')
                            .build())

        self.creature2 = (CharacterBuilder()
                            .with_tick(0)
                            .with_speed(2)
                            .with_name('creature 2')
                            .build())

        self.creature3 = (CharacterBuilder()
                            .with_tick(3)
                            .with_speed(0.5)
                            .with_name('creature 3')
                            .build())

        self.model = Model()
        self.model.dungeon = Dungeon()
        self.model.dungeon.levels = Level((20, 20), 0, 0)

        self.model.dungeon.levels.add_creature(self.creature1)
        self.model.dungeon.levels.add_creature(self.creature2)
        self.model.player = self.creature3
        self.model.dungeon.levels.add_creature(self.creature3)

    def test_get_next_zero_tick(self):
        """
        Test that system can tell whose turn it is to act
        One creature has tick of 0
        """
        creature = self.model.get_next_creature()
        assert_that(creature, is_(equal_to(self.creature2)))

    def test_get_next_positive_tick(self):
        """
        Test that system can tell whose turn it is to act
        All creatures have positive tick
        """
        self.creature1.tick = 5
        self.creature2.tick = 10
        self.creature3.tick = 3
        creature = self.model.get_next_creature()
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
        self.creature = (CharacterBuilder()
                            .with_tick(5)
                            .build())

        self.model = Model()
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
        self.creature.add_effect(effect)

        next_creature = self.model.get_next_creature()

        verify(effect).trigger()

    def test_tick_will_be_reset(self):
        """
        Test that tick of effect will be reset after it has been triggered
        """
        effect = Effect(duration = 50,
                        frequency = 5,
                        tick = 5)
        self.creature.add_effect(effect)

        next_creature = self.model.get_next_creature()
        effect = self.creature.get_effects()[0]

        assert_that(effect.tick, is_(equal_to(5)))

    def test_effects_will_stay_in_sync(self):
        """
        Test that two effects will stay in sync
        """
        effect1 = Effect(duration = 50,
                        frequency = 5,
                        tick = 5)

        self.creature.add_effect(effect1)

        effect2 = Effect(duration = 50,
                         frequency = 5,
                         tick = 5)

        creature2 = (CharacterBuilder()
                        .with_tick(10)
                        .with_effect_handle(effect2)
                        .with_level(self.level)
                        .build()
                        )


        self.level.creatures = [self.creature,
                                creature2]

        next_creature = self.model.get_next_creature()
        assert_that(effect1.tick, is_(equal_to(effect2.tick)))

        next_creature.tick = 10
        next_creature = self.model.get_next_creature()
        assert_that(effect1.tick, is_(equal_to(effect2.tick)))

    def test_effects_duration_goes_down(self):
        """
        Test that duration of effect is gradually counted down
        """
        effect = Effect(duration = 50,
                        frequency = 5,
                        tick = 5)

        self.creature.add_effect(effect)

        next_creature = self.model.get_next_creature()

        assert_that(effect.duration, is_(equal_to(45)))

    def test_expired_effects_are_removed(self):
        """
        Test that expired effects are removed
        """
        creature = (CharacterBuilder()
                        .with_tick(5)
                        .with_level(self.level)
                        .build())

        self.model.player = creature
        self.level.creatures = [creature]

        effect = Effect(duration = 5,
                        frequency = 5,
                        tick = 5)

        creature.add_effect(effect)

        next_creature = self.model.get_next_creature()

        assert_that(creature.get_effects(), is_not(has_item(effect)))

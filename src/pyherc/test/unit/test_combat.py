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
Module for testing combat related rules
"""
#pylint: disable=W0614
import pyherc
from pyherc.data import Character
from pyherc.data import Dungeon
from pyherc.data import Model

from pyherc.rules.public import AttackParameters
from pyherc.rules.attack.action import AttackAction
from pyherc.events import AttackNothingEvent, AttackHitEvent, AttackMissEvent

from pyherc.test.builders import CharacterBuilder
from pyherc.test.builders import ActionFactoryBuilder
from pyherc.test.builders import LevelBuilder

from pyherc.test.cutesy import at_

from mockito import mock, verify, when, any
from hamcrest import * #pylint: disable=W0401

class TestMeleeCombat(object):
    """
    Class for testing melee combat related rules
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestMeleeCombat, self).__init__()
        self.level = None
        self.modle = None
        self.character1 = None
        self.character2 = None
        self.observer = None
        self.action_factory = None

    def setup(self):
        """
        Setup for testcases
        """
        self.model = Model()

        self.action_factory = (ActionFactoryBuilder()
                                    .with_attack_factory()
                                    .build())

        self.character1 = (CharacterBuilder()
                                .with_model(self.model)
                                .with_hit_points(10)
                                .with_attack(3)
                                .with_body(5)
                                .build())

        self.character2 = (CharacterBuilder()
                                .with_model(self.model)
                                .with_hit_points(10)
                                .with_attack(3)
                                .with_body(5)
                                .build())

        self.observer = mock()
        when(self.observer).build().thenReturn(self.observer)

        self.model.dungeon = Dungeon()
        self.level = (LevelBuilder()
                        .with_character(self.character1, at_(5, 5))
                        .with_character(self.character2, at_(6, 5))
                        .with_character(self.observer, at_(2, 3))
                        .build())

        self.model.dungeon.levels = self.level

    def test_get_unarmed_action(self):
        """
        Test that unarmed combat action can be generated
        """
        rng = mock()

        action = self.action_factory.get_action(AttackParameters(
                                                      self.character1,
                                                      3,
                                                      'unarmed',
                                                      rng))

        assert_that(action, is_(instance_of(AttackAction)))
        assert_that(action.attack_type, is_(equal_to('unarmed')))

    def test_unarmed_attack_hit_event(self):
        """
        Test that landing an unarmed hit will raise correct event
        """
        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        self.character1.perform_attack(3,
                                       self.action_factory,
                                       rng)

        verify(self.observer).receive_event(any(AttackHitEvent))

    def test_unarmed_attack_miss_event(self):
        """
        Test that landing an unarmed miss will raise correct event
        """
        rng = mock()
        when(rng).randint(1, 6).thenReturn(6)

        self.character1.perform_attack(3,
                                       self.action_factory,
                                       rng)

        verify(self.observer).receive_event(any(AttackMissEvent))

    def test_attack_into_air_raises_event(self):
        """
        Attacks into thin air should raise correct event
        """
        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        self.character1.perform_attack(1,
                                       self.action_factory,
                                       rng)

        verify(self.observer).receive_event(any(AttackNothingEvent))

    def test_attacking_to_enter_direction_is_treated_like_attacking_air(self):
        """
        Attacking through portal should be treated like attacking into air
        """
        action = self.action_factory.get_action(AttackParameters(
                                                      self.character1,
                                                      9,
                                                      'unarmed',
                                                      mock()))

        assert_that(action.target, is_(equal_to(None)))

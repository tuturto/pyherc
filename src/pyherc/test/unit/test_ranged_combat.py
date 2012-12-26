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
Module for testing ranged combat related rules
"""
from pyherc.rules.attack import RangedCombatFactory
from pyherc.rules.public import AttackParameters
from pyherc.test.matchers import AttackActionParameterMatcher
from pyherc.test.builders import LevelBuilder, CharacterBuilder, ItemBuilder
from mockito import verify, mock, when, any
from hamcrest import assert_that, is_, equal_to
from random import Random

class TestRangedCombat(object):
    """
    Tests for ranged combat
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestRangedCombat, self).__init__()

        self.level = None
        self.character = None
        self.target = None
        self.action_factory = None

    def setup(self):
        """
        Setup test cases
        """
        self.character = (CharacterBuilder()
                            .with_location((2, 2))
                            .build())

        self.target = (CharacterBuilder()
                            .with_location((5, 2))
                            .build())

        self.level = (LevelBuilder()
                        .with_character(self.character)
                        .with_character(self.target)
                        .build())

        bow = (ItemBuilder()
                    .with_name('bow')
                    .with_required_ammunition_type('arrow')
                    .build())
        arrows = (ItemBuilder()
                        .with_name('arrows')
                        .with_ammunition_type('arrow')
                        .build())

        self.character.inventory.weapon = bow
        self.character.inventory.projectiles = arrows

        self.action_factory = mock()
        when(self.action_factory).get_action(any()).thenReturn(mock())

    def test_ranged_attack_is_created_for_distant_enemy(self):
        """
        When attacking enemy in distance, a ranged attack should
        be created
        """
        self.character.perform_attack(3,
                                      self.action_factory,
                                      Random())

        verify(self.action_factory).get_action(
                            AttackActionParameterMatcher(
                                        attack_type = 'ranged'))

    def test_melee_attack_is_created_for_close_enemy(self):
        """
        Even when character is armed with ranged weapon, he can not use
        ranged attack against enemy that is standing right next to him
        """
        self.target.location = (self.character.location[0] + 1,
                                self.character.location[1])

        self.character.perform_attack(3,
                                      self.action_factory,
                                      Random())

        verify(self.action_factory).get_action(
                            AttackActionParameterMatcher(
                                        attack_type = 'melee'))

    def test_finding_target(self):
        """
        Test that factory can find the target
        """
        factory = RangedCombatFactory(effect_factory = mock(),
                                      dying_rules = mock())

        target = factory.get_target(
                            AttackParameters(
                                        attacker = self.character,
                                        direction = 3,
                                        attack_type = 'ranged',
                                        random_number_generator = Random()))

        assert_that(target, is_(equal_to(self.target)))

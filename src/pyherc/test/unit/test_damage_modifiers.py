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
Module for testing damage modification rules
"""
from pyherc.data import Model,  Dungeon
from pyherc.test.builders import ActionFactoryBuilder
from pyherc.test.builders import CharacterBuilder, LevelBuilder, ItemBuilder
from pyherc.data.effects import DamageModifier

from pyherc.test.cutesy import at_

from mockito import mock, when

from hamcrest import assert_that, is_, equal_to

class TestDamageModifiers(object):
    """
    Tests for damage modifier effect
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestDamageModifiers, self).__init__()
        self.level = None
        self.modle = None
        self.character1 = None
        self.character2 = None
        self.action_factory = None
        self.rng = None

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

        self.effect = DamageModifier(modifier = 1,
                                     damage_type = 'crushing',
                                     duration = None,
                                     frequency = None,
                                     tick = None,
                                     icon = 101,
                                     title = 'Weakness against crushing',
                                     description = 'This character is weak')
        self.effect.multiple_allowed = True

        self.character2 = (CharacterBuilder()
                                .with_model(self.model)
                                .with_hit_points(10)
                                .with_attack(3)
                                .with_body(5)
                                .with_effect(self.effect)
                                .build())

        self.model.dungeon = Dungeon()
        self.level = (LevelBuilder()
                        .with_character(self.character1, at_(5, 5))
                        .with_character(self.character2, at_(6, 5))
                        .build())

        self.model.dungeon.levels = self.level

        self.rng = mock()
        when(self.rng).randint(1, 6).thenReturn(1)

    def test_damage_is_increased(self):
        """
        Test that suffered damage can be modified
        """
        self.character1.perform_attack(3,
                                       self.action_factory,
                                       self.rng)

        assert_that(self.character2.hit_points, is_(equal_to(6)))

    def test_non_matching_damage_increase_is_not_done(self):
        """
        Test that suffered damage is not modified when modifier does not
        match with the damage
        """
        self.effect.damage_type = 'slashing'

        self.character1.perform_attack(3,
                                       self.action_factory,
                                       self.rng)

        assert_that(self.character2.hit_points, is_(equal_to(7)))

    def test_multiple_modifiers_are_handled(self):
        """
        Test that multiple modifier are taken into account and not skipped
        """
        effect_2 = DamageModifier(modifier = 3,
                                  damage_type = 'crushing',
                                  duration = None,
                                  frequency = None,
                                  tick = None,
                                  icon = 101,
                                  title = 'title',
                                  description = 'description')
        effect_2.multiple_allowed = True
        self.character2.add_effect(effect_2)

        self.character1.perform_attack(3,
                                       self.action_factory,
                                       self.rng)

        assert_that(self.character2.hit_points, is_(equal_to(3)))

    def test_melee_combat_is_handled(self):
        """
        Damage modifiers should be handled in melee combat too
        """
        weapon = (ItemBuilder()
                        .with_name('hammer')
                        .with_damage(2, 'crushing')
                        .build())

        self.character1.inventory.weapon = weapon

        self.character1.perform_attack(3,
                                       self.action_factory,
                                       self.rng)

        assert_that(self.character2.hit_points, is_(equal_to(7)))

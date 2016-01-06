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
Module for testing damage modification rules
"""
from hamcrest import assert_that, equal_to, is_
from mockito import mock, when
from pyherc.data import Dungeon, Model
from pyherc.data.effects import DamageModifier
from pyherc.ports import attack, set_action_factory
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  ItemBuilder, LevelBuilder)
from pyherc.test.cutesy import at_


class TestDamageModifiers():
    """
    Tests for damage modifier effect
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.level = None
        self.modle = None
        self.character1 = None
        self.character2 = None
        self.rng = None

    def setup(self):
        """
        Setup for testcases
        """
        self.model = Model()

        set_action_factory(ActionFactoryBuilder()
                           .with_attack_factory()
                           .build())

        self.character1 = (CharacterBuilder()
                           .with_model(self.model)
                           .with_hit_points(10)
                           .with_attack(3)
                           .with_body(5)
                           .build())

        self.effect = DamageModifier(modifier=1,
                                     damage_type='crushing',
                                     duration=None,
                                     frequency=None,
                                     tick=None,
                                     icon=101,
                                     title='Weakness against crushing',
                                     description='This character is weak')
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
        attack(self.character1,
               3,
               self.rng)

        assert_that(self.character2.hit_points, is_(equal_to(6)))

    def test_non_matching_damage_increase_is_not_done(self):
        """
        Test that suffered damage is not modified when modifier does not
        match with the damage
        """
        self.effect.damage_type = 'slashing'

        attack(self.character1,
               3,
               self.rng)

        assert_that(self.character2.hit_points, is_(equal_to(7)))

    def test_multiple_modifiers_are_handled(self):
        """
        Test that multiple modifier are taken into account and not skipped
        """
        effect_2 = DamageModifier(modifier=3,
                                  damage_type='crushing',
                                  duration=None,
                                  frequency=None,
                                  tick=None,
                                  icon=101,
                                  title='title',
                                  description='description')
        effect_2.multiple_allowed = True
        self.character2.add_effect(effect_2)

        attack(self.character1,
               3,
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

        attack(self.character1,
               3,
               self.rng)

        assert_that(self.character2.hit_points, is_(equal_to(7)))

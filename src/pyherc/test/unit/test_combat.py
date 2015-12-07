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
Module for testing combat related rules
"""
from hamcrest import assert_that, equal_to, instance_of, is_
from mockito import any, mock, verify, when
from pyherc.data import Dungeon, Model
from pyherc.rules import attack
from pyherc.rules.combat.action import AttackAction
from pyherc.rules.combat.interface import AttackParameters
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  LevelBuilder)
from pyherc.test.cutesy import at_
from pyherc.test.matchers import void_target


class TestMeleeCombat():
    """
    Class for testing melee combat related rules
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

        action = self.action_factory.get_action(
            AttackParameters(self.character1,
                             3,
                             'unarmed',
                             rng))

        assert_that(action, is_(instance_of(AttackAction)))
        assert_that(action.attack_type, is_(equal_to('unarmed')))

    def test_attacking_to_enter_direction_is_treated_like_attacking_air(self):
        """
        Attacking through portal should be treated like attacking into air
        """
        action = self.action_factory.get_action(
            AttackParameters(self.character1,
                             9,
                             'unarmed',
                             mock()))

        assert_that(action.target, is_(void_target()))

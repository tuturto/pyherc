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
Module for testing ranged combat related rules
"""
from random import Random

from hamcrest import assert_that, equal_to, is_, is_not
from mockito import any, mock, verify, when
from pyherc.ports import attack, set_action_factory
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  ItemBuilder, LevelBuilder)
from pyherc.test.matchers import does_have
from pyherc.data import wall_tile, add_character, remove_character
from pyherc.data import move_character


class TestRangedCombat():
    """
    Tests for ranged combat
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.level = None
        self.character = None
        self.target = None

    def setup(self):
        """
        Setup test cases
        """
        self.character = (CharacterBuilder()
                            .with_hit_points(10)
                            .build())

        self.target = (CharacterBuilder()
                            .with_hit_points(10)
                            .build())

        self.level = (LevelBuilder()
                        .build())

        add_character(self.level, (2, 2), self.character)
        add_character(self.level, (5, 2), self.target)

        bow = (ItemBuilder()
                    .with_name('bow')
                    .with_required_ammunition_type('arrow')
                    .with_damage(1, 'crushing')
                    .build())
        self.arrows = (ItemBuilder()
                        .with_name('arrows')
                        .with_ammunition_type('arrow')
                        .with_range_damage(3, 'piercing')
                        .with_count(10)
                        .build())

        self.character.inventory.append(bow)
        self.character.inventory.append(self.arrows)
        self.character.inventory.weapon = bow
        self.character.inventory.projectiles = self.arrows

        set_action_factory(ActionFactoryBuilder()
                           .with_attack_factory()
                           .build())

    def test_damage_for_ranged_attack_is_from_arrow(self):
        """
        Damage for ranged attack comes from the arrow
        """
        attack(self.character,
               3,
               Random())

        assert_that(self.target.hit_points, is_(equal_to(7)))

    def test_ammunition_is_decreased(self):
        """
        Ranged attack should use ammunition
        """
        attack(self.character,
               3,
               Random())

        assert_that(self.arrows.ammunition_data.count, is_(equal_to(9)))

    def test_depleted_ammunition_is_removed(self):
        """
        Completely spent ammunition should be removed from inventory
        """
        self.arrows.ammunition_data.count = 1

        attack(self.character,
               3,
               Random())

        assert_that(self.character, is_not(does_have(self.arrows)))

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
Module for testing attack action related classes
"""
from hamcrest import assert_that, equal_to, is_
from mockito import any, mock, verify, when
from pyherc.data.geometry import TargetData
from pyherc.data.damage import new_damage
from pyherc.test.builders import (CharacterBuilder, EffectHandleBuilder,
                                  ItemBuilder)


class TestDamage():
    """
    Tests for damage
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestDamage, self).__init__()

    def test_negative_damage_is_zeroed(self):
        """
        Test that damage below zero is zeroed
        """
        character = CharacterBuilder().build()
        damage = new_damage([(-1, 'negative damage')])

        damage_inflicted = damage(target=character)

        assert_that(damage_inflicted[0], is_(equal_to(0)))

    def test_armour_is_used(self):
        """
        Test that armoud used by target is used
        """
        character = CharacterBuilder().build()

        armour = ItemBuilder().build()
        armour.armour_data = mock()
        armour.armour_data.damage_reduction = 1
        character.inventory.armour = armour

        damage = new_damage([(5, 'crushing')])

        damage_inflicted = damage(target=character)

        assert_that(damage_inflicted[0], is_(equal_to(4)))

    def test_less_than_double_protection_is_not_negated(self):
        """
        Damage that is less than protection, but higher than
        half of the protection should deal 1 point of damage
        """
        character = CharacterBuilder().build()

        armour = ItemBuilder().build()
        armour.armour_data = mock()
        armour.armour_data.damage_reduction = 3
        character.inventory.armour = armour

        damage = new_damage([(2, 'crushing')])

        damage_inflicted = damage(target=character)

        assert_that(damage_inflicted[0], is_(equal_to(1)))

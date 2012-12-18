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
Module for testing attack action related classes
"""
from pyherc.rules.attack.action import Damage
from pyherc.test.builders import CharacterBuilder, ItemBuilder
from hamcrest import assert_that, is_, equal_to
from mockito import mock, verify

class TestDamage(object):
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
        character = (CharacterBuilder()
                        .build())
        damage = Damage([(-1, 'negative damage')])

        damage.apply_damage(target = character)

        assert_that(damage.damage_inflicted, is_(equal_to(0)))

    def test_armour_is_used(self):
        """
        Test that armoud used by target is used
        """
        character = (CharacterBuilder()
                        .build())

        armour = ItemBuilder().build()
        armour.armour_data = mock()
        armour.armour_data.damage_reduction = 1
        character.inventory.armour = armour

        damage = Damage([(5, 'crushing')])

        damage.apply_damage(target = character)

        assert_that(damage.damage_inflicted, is_(equal_to(4)))

    def test_less_than_double_protection_is_not_negated(self):
        """
        Damage that is less than protection, but higher than
        half of the protection should deal 1 point of damage
        """
        character = (CharacterBuilder()
                        .build())

        armour = ItemBuilder().build()
        armour.armour_data = mock()
        armour.armour_data.damage_reduction = 3
        character.inventory.armour = armour

        damage = Damage([(2, 'crushing')])

        damage.apply_damage(target = character)

        assert_that(damage.damage_inflicted, is_(equal_to(1)))
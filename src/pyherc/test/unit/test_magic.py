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
Module for magic related tests
"""
#pylint: disable=W0614
from pyherc.rules.effects import Heal, Damage
from pyherc.test.builders import CharacterBuilder
from hamcrest import * #pylint: disable=W0401

class TestMagic:
    """
    Tests for magic
    """

    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_damage_effect(self):
        """
        Test that a damage effect can be applied on a character
        """
        character = (CharacterBuilder()
                        .with_hit_points(15)
                        .with_max_hp(15)
                        .build())

        effect = Damage(duration = 0,
                        frequency = 0,
                        tick = 0,
                        damage = 10,
                        target = character)

        effect.trigger()

        assert_that(character.hit_points, is_(equal_to(5)))

    def test_healing_effect(self):
        """
        Test that a healing effect can be applied on a character
        """
        character = (CharacterBuilder()
                        .with_hit_points(1)
                        .with_max_hp(15)
                        .build())

        effect = Heal(duration = 0,
                      frequency = 0,
                      tick = 0,
                      healing = 10,
                      target = character)
        effect.trigger()

        assert_that(character.hit_points, is_(equal_to(11)))

    def test_healing_does_not_heal_over_max_hp(self):
        """
        Test that character does not get healed over his maximum hp when getting healing effect
        """
        character = (CharacterBuilder()
                        .with_hit_points(1)
                        .with_max_hp(5)
                        .build())

        effect = Heal(duration = 0,
                      frequency = 0,
                      tick = 0,
                      healing = 10,
                      target = character)

        effect.trigger()

        assert_that(character.hit_points, is_(equal_to(5)))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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

import pyherc
import pyherc.rules.magic
import pyherc.data.model
from pyherc.data.item import Item
from pyherc.data.item import ItemEffectData
from pyherc.test import IntegrationTest
from pyherc.test import StubModel

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
        model = StubModel()
        character = pyherc.data.model.Character(None)
        character.hit_points = 15
        character.max_hp = 15
        pyherc.rules.magic.cast_effect(
                            model, character,
                            ItemEffectData('on drink', 'damage', '1d10'), [10])

        assert(character.hit_points == 5)

    def test_healing_effect(self):
        """
        Test that a healing effect can be applied on a character
        """
        model = StubModel()
        character = pyherc.data.model.Character(None)
        character.hit_points = 1
        character.max_hp = 15
        pyherc.rules.magic.cast_effect(
                            model, character,
                            ItemEffectData('on drink', 'healing', '1d10'), [10])

        assert(character.hit_points == 11)

    def test_healing_does_not_heal_over_max_hp(self):
        """
        Test that character does not get healed over his maximum hp when getting healing effect
        """
        model = StubModel()
        character = pyherc.data.model.Character(None)
        character.hit_points = 1
        character.max_hp = 5
        pyherc.rules.magic.cast_effect(
                        model, character,
                        ItemEffectData('on drink', 'healing', '1d10'), [10])

        assert(character.hit_points == 5)


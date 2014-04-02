# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
Module for testing wearing armour
"""

from hamcrest import assert_that  # pylint: disable-msg=E0611
from pyherc.rules import equip
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  ItemBuilder)
from pyherc.test.matchers import is_wearing


class TestWearingArmour():
    """
    Tests for wearing armour
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestWearingArmour, self).__init__()

    def test_wear_armour(self):
        """
        Test that armour can be worn
        """
        character = CharacterBuilder().build()

        armour = (ItemBuilder()
                        .with_damage_reduction(2)
                        .with_speed_modifier(1)
                        .with_name('leather armour')
                        .build())

        action_factory = (ActionFactoryBuilder()
                                .with_inventory_factory()
                                .build())

        equip(character,
              armour,
              action_factory)

        assert_that(character, is_wearing(armour))

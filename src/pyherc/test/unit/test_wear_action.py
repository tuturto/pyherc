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
Module for testing wearing armour
"""

from hamcrest import assert_that, is_not  # pylint: disable-msg=E0611
from pyherc.ports import equip, unequip, set_action_factory
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  ItemBuilder)
from pyherc.test.matchers import is_wearing_armour, is_wearing_boots


class TestWearingArmour():
    """
    Tests for wearing armour
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestWearingArmour, self).__init__()

    def setup(self):
        """
        Setup test case
        """
        set_action_factory(ActionFactoryBuilder()
                           .with_inventory_factory()
                           .build())        

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

        
        equip(character, armour)

        assert_that(character, is_wearing_armour(armour))

    def test_wear_boots(self):
        """
        Test that boots can be worn
        """
        character = CharacterBuilder().build()

        boots = (ItemBuilder()
                 .with_name('boots')
                 .with_boots_speed_modifier(1)
                 .build())

        equip(character, boots)

        assert_that(character, is_wearing_boots(boots))

    def test_taking_off_boots(self):
        """
        Boots can be removed
        """
        character = CharacterBuilder().build()

        boots = (ItemBuilder()
                 .with_name('boots')
                 .with_boots_speed_modifier(1)
                 .build())

        character.inventory.boots = boots

        unequip(character, boots)

        assert_that(character, is_not(is_wearing_boots(boots)))

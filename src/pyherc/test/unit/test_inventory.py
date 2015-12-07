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

from hamcrest import (assert_that,  # pylint: disable-msg=E0611; pylint: disable-msg=E0611
                      equal_to, is_, is_in, is_not, none, not_none)
from mockito import mock
from pyherc.test.builders import CharacterBuilder

"""
Tests for Inventory
"""
class TestInventory():
    """
    Tests for inventory
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.character = CharacterBuilder().build()

    def test_lenght_of_empty_inventory(self):
        """
        Test that length of empty inventory is reported correctly
        """
        assert_that(len(self.character.inventory), is_(equal_to(0)))

    def test_lenght_of_one_item_inventory(self):
        """
        Test that length of one item inventory is reported correctly
        """
        self.character.inventory.append(mock())

        assert_that(len(self.character.inventory), is_(equal_to(1)))

    def test_accessing_items(self):
        """
        Test that items can be added and retrieved from inventory
        """
        item_1 = mock()
        item_2 = mock()

        self.character.inventory.append(item_1)

        assert_that(self.character.inventory[0], is_(equal_to(item_1)))

        self.character.inventory[0] = item_2

        assert_that(self.character.inventory[0], is_(equal_to(item_2)))

    def test_deleting_items(self):
        """
        Test that item can be deleted from inventory
        """
        item = mock()

        self.character.inventory.append(item)

        assert_that(item, is_in(self.character.inventory))

        del self.character.inventory[0]

        assert_that(item, is_not(is_in(self.character.inventory)))

    def test_removing_items(self):
        """
        Test that item can be removed from inventory
        """
        item = mock()

        self.character.inventory.append(item)

        assert_that(item, is_in(self.character.inventory))

        self.character.inventory.remove(item)

        assert_that(item, is_not(is_in(self.character.inventory)))

    def test_getting_iterator(self):
        """
        Test that iterator can be produced
        """
        item = mock()

        self.character.inventory.append(item)

        iterator = self.character.inventory.__iter__()

        assert_that(iterator, is_(not_none()))

    def test_removing_weapon_in_use(self):
        """
        Test that weapon in use is removed when dropped
        """
        item = mock()

        self.character.inventory.append(item)
        self.character.inventory.weapon = item

        self.character.inventory.remove(item)

        assert_that(self.character.inventory.weapon, is_(none()))

    def test_deleting_weapon_in_use(self):
        """
        Test that deleting weapon in use from inventory removes it from use
        """
        item = mock()

        self.character.inventory.append(item)
        self.character.inventory.weapon = item

        del self.character.inventory[0]

        assert_that(self.character.inventory.weapon, is_(none()))

    def test_armour_in_use(self):
        """
        Test that removing armour in use removes it from use
        """
        item = mock()

        self.character.inventory.append(item)
        self.character.inventory.armour = item

        self.character.inventory.remove(item)

        assert_that(self.character.inventory.armour, is_(none()))

    def test_projectiles_in_use(self):
        """
        Test that removing projectiles in use removes it from use
        """
        item = mock()

        self.character.inventory.append(item)
        self.character.inventory.projectiles = item

        self.character.inventory.remove(item)

        assert_that(self.character.inventory.projectiles, is_(none()))

    def test_deleting_boots_in_use(self):
        """
        Worn boots should be removed from use when removed from inventory
        """
        item = mock()

        self.character.inventory.append(item)
        self.character.inventory.boots = item

        self.character.inventory.remove(item)

        assert_that(self.character.inventory.boots, is_(none()))

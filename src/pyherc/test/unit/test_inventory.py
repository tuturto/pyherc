#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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

from pyherc.data import Inventory
from hamcrest import assert_that, is_,  equal_to, is_in, not_none, is_not
from hamcrest import none
from mockito import mock

"""
Tests for Inventory
"""
class TestInventory(object):
    """
    Tests for inventory
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestInventory, self).__init__()

    def test_lenght_of_empty_inventory(self):
        """
        Test that length of empty inventory is reported correctly
        """
        inventory = Inventory()

        assert_that(len(inventory), is_(equal_to(0)))

    def test_lenght_of_one_item_inventory(self):
        """
        Test that length of one item inventory is reported correctly
        """
        inventory = Inventory()

        inventory.append(mock())

        assert_that(len(inventory), is_(equal_to(1)))

    def test_accessing_items(self):
        """
        Test that items can be added and retrieved from inventory
        """
        inventory = Inventory()
        item_1 = mock()
        item_2 = mock()

        inventory.append(item_1)

        assert_that(inventory[0], is_(equal_to(item_1)))

        inventory[0] = item_2

        assert_that(inventory[0], is_(equal_to(item_2)))

    def test_deleting_items(self):
        """
        Test that item can be deleted from inventory
        """
        inventory = Inventory()
        item = mock()

        inventory.append(item)

        assert_that(item, is_in(inventory))

        del inventory[0]

        assert_that(item, is_not(is_in(inventory)))

    def test_removing_items(self):
        """
        Test that item can be removed from inventory
        """
        inventory = Inventory()
        item = mock()

        inventory.append(item)

        assert_that(item, is_in(inventory))

        inventory.remove(item)

        assert_that(item, is_not(is_in(inventory)))

    def test_getting_iterator(self):
        """
        Test that iterator can be produced
        """
        inventory = Inventory()
        item = mock()

        inventory.append(item)

        iterator = inventory.__iter__()

        assert_that(iterator, is_(not_none()))

    def test_removing_weapon_in_use(self):
        """
        Test that weapon in use is removed when dropped
        """
        inventory = Inventory()
        item = mock()

        inventory.append(item)
        inventory.weapon = item

        inventory.remove(item)

        assert_that(inventory.weapon, is_(none()))

    def test_deleting_weapon_in_use(self):
        """
        Test that deleting weapon in use from inventory removes it from use
        """
        inventory = Inventory()
        item = mock()

        inventory.append(item)
        inventory.weapon = item

        del inventory[0]

        assert_that(inventory.weapon, is_(none()))

    def test_armour_in_use(self):
        """
        Test that removing armour in use removes it from use
        """
        inventory = Inventory()
        item = mock()

        inventory.append(item)
        inventory.armour = item

        inventory.remove(item)

        assert_that(inventory.armour, is_(none()))

    def test_projectiles_in_use(self):
        """
        Test that removing projectiles in use removes it from use
        """
        inventory = Inventory()
        item = mock()

        inventory.append(item)
        inventory.projectiles = item

        inventory.remove(item)

        assert_that(inventory.projectiles, is_(none()))

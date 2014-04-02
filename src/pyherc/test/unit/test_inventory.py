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

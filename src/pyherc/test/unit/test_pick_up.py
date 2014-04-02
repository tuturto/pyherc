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
Tests for pick up action
"""
from hamcrest import assert_that, equal_to, is_  # pylint: disable-msg=E0611
from mockito import any, mock, verify
from pyherc.data import Model
from pyherc.events import PickUpEvent
from pyherc.rules import pick_up
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  ItemBuilder, LevelBuilder)


class TestPickingUp():
    """
    Tests for picking up itmes
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestPickingUp, self).__init__()

        self.item = None
        self.level = None
        self.character = None
        self.action_factory = None

    def setup(self):
        """
        Setup test cases
        """
        self.item = (ItemBuilder()
                        .build())

        self.model = Model()

        self.level = LevelBuilder().build()

        self.character = (CharacterBuilder()
                            .with_location((5, 5))
                            .with_level(self.level)
                            .with_model(self.model)
                            .build())

        self.level.add_item(self.item, (5, 5))

        self.action_factory = (ActionFactoryBuilder()
                                    .with_inventory_factory()
                                    .build())

    def test_picking_up(self):
        """
        Test that item can be picked up
        """
        pick_up(self.character,
                self.item,
                self.action_factory)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)
        assert(self.item.location == ())

    def test_picking_up_raises_event(self):
        """
        Event should be raised when item is picked up
        """
        observer = mock()

        self.level.add_creature(observer, (1, 1))

        pick_up(self.character,
                self.item,
                self.action_factory)

        verify(observer).receive_event(any(PickUpEvent))

    def test_picking_up_not_correct_location(self): #pylint: disable=C0103
        """
        Test that item is not picked up from wrong location
        """
        self.character.location = (6, 6)

        assert(self.character.location == (6, 6))
        assert(self.item.location == (5, 5))

        pick_up(self.character,
                self.item,
                self.action_factory)

        assert(not self.item in self.character.inventory)
        assert(self.item in self.level.items)

    def test_merging_ammunition_in_pickup(self):
        """
        Same kind of ammunition should be merged when picked up
        """
        ammo_1 = (ItemBuilder()
                    .with_name('arrow')
                    .with_count(10)
                    .build())
        ammo_2 = (ItemBuilder()
                    .with_name('arrow')
                    .with_count(20)
                    .build())

        self.level.add_item(ammo_1, self.character.location)
        self.level.add_item(ammo_2, self.character.location)

        pick_up(self.character,
                ammo_1,
                self.action_factory)
        pick_up(self.character,
                ammo_2,
                self.action_factory)

        assert_that(len(self.character.inventory), is_(equal_to(1)))

        item = self.character.inventory[0]

        assert_that(item.ammunition_data.count, is_(equal_to(30)))

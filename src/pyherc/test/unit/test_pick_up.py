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
Tests for pick up action
"""
from hamcrest import assert_that, equal_to, is_  # pylint: disable-msg=E0611
from mockito import any, mock, verify
from pyherc.data import Model, add_item, get_items
from pyherc.ports import pick_up, set_action_factory
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

        add_item(self.level, (5, 5), self.item)

        set_action_factory(ActionFactoryBuilder()
                           .with_inventory_factory()
                           .build())

    def test_picking_up(self):
        """
        Test that item can be picked up
        """
        pick_up(self.character,
                self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in get_items(self.level))
        assert(self.item.location == ())

    def test_picking_up_not_correct_location(self): #pylint: disable=C0103
        """
        Test that item is not picked up from wrong location
        """
        self.character.location = (6, 6)

        assert(self.character.location == (6, 6))
        assert(self.item.location == (5, 5))

        pick_up(self.character,
                self.item)

        assert(not self.item in self.character.inventory)
        assert(self.item in get_items(self.level))

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

        add_item(self.level, self.character.location, ammo_1)
        add_item(self.level, self.character.location, ammo_2)

        pick_up(self.character,
                ammo_1)
        pick_up(self.character,
                ammo_2)

        assert_that(len(self.character.inventory), is_(equal_to(1)))

        item = self.character.inventory[0]

        assert_that(item.ammunition_data.count, is_(equal_to(30)))

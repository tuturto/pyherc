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
Module for testing drop action factory
"""
from hamcrest import assert_that, equal_to, greater_than, is_, is_in, is_not
from mockito import any, mock, verify
from pyherc.data import Model
from pyherc.rules import drop_item
from pyherc.rules.inventory.factories import DropFactory
from pyherc.rules.inventory.interface import InventoryParameters
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  ItemBuilder, LevelBuilder)
from pyherc.test.matchers import event_type_of


class TestDropFactory():
    """
    Tests for drop action factory
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_can_handle_parameters(self):
        """
        Test that drop factory can handle parameter class
        """
        parameters = InventoryParameters(character=mock(),
                                         item=mock(),
                                         sub_action='drop')
        factory = DropFactory()

        can_handle = factory.can_handle(parameters)

        assert_that(can_handle, is_(equal_to(True)))


class TestDropAction():
    """
    Tests for dropping item
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.item = None
        self.level = None
        self.character = None
        self.action_factory = None
        self.model = None

    def setup(self):
        """
        Setup test case
        """
        self.model = mock(Model)
        self.level = LevelBuilder().build()
        self.item = ItemBuilder().build()

        self.character = (CharacterBuilder()
                          .with_item(self.item)
                          .with_level(self.level)
                          .with_location((5, 5))
                          .with_model(self.model)
                          .build())

        self.action_factory = (ActionFactoryBuilder()
                               .with_inventory_factory()
                               .build())

    def test_dropped_item_is_removed_from_inventory(self):
        """
        Test that dropped item is removed from inventory
        """
        drop_item(self.character,
                  self.item,
                  self.action_factory)

        assert_that(self.item,
                    is_not(is_in(self.character.inventory)))

    def test_dropped_item_is_added_on_level(self):
        """
        Test that dropped item ends up on level
        """
        drop_item(self.character,
                  self.item,
                  self.action_factory)

        assert_that(self.item.level,
                    is_(equal_to(self.level)))

    def test_dropped_item_added_to_correct_location(self):
        """
        Test that dropped item is added to correct location
        """
        drop_item(self.character,
                  self.item,
                  self.action_factory)

        assert_that(self.item.location,
                    is_(equal_to(self.character.location)))

    def test_dropping_takes_time(self):
        """
        Dropping an item should move characters time forward
        """
        old_time = self.character.tick

        drop_item(self.character,
                  self.item,
                  self.action_factory)
        new_time = self.character.tick

        assert_that(new_time, is_(greater_than(old_time)))

    def test_dropping_raises_event(self):
        """
        Dropping an item should raise an event
        """
        drop_item(self.character,
                  self.item,
                  self.action_factory)

        verify(self.model).raise_event(event_type_of('drop'))

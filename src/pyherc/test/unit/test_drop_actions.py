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
Module for testing drop action factory
"""
from pyherc.rules.inventory.factories import DropFactory
from pyherc.rules import InventoryParameters
from pyherc.test.builders import ItemBuilder, CharacterBuilder
from pyherc.test.builders import ActionFactoryBuilder

from mockito import mock
from hamcrest import assert_that, is_, equal_to, is_in, is_not

class TestDropFactory(object):
    """
    Tests for drop action factory
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestDropFactory, self).__init__()

    def test_can_handle_parameters(self):
        """
        Test that drop factory can handle parameter class
        """
        parameters = InventoryParameters(character = mock(),
                                         item = mock(),
                                         sub_action = 'drop')
        factory = DropFactory()

        can_handle = factory.can_handle(parameters)

        assert_that(can_handle, is_(equal_to(True)))

    def test_dropped_item_is_removed_from_inventory(self):
        """
        Test that dropped item is removed from inventory
        """
        item = ItemBuilder().build()
        character = (CharacterBuilder()
                        .with_item(item)
                        .build())
        action_factory = (ActionFactoryBuilder()
                            .with_inventory_factory()
                            .build())

        character.drop_item(item, action_factory)

        assert_that(item, is_not(is_in(character.inventory)))

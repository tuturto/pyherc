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
Package for inventory tests
"""

from herculeum.gui import InventoryDialog
from herculeum.gui.surfaceManager import SurfaceManager
from pyherc.rules import ActionFactory
import herculeum.gui.resources
from herculeum.test.matchers import slot_with_item

from mockito import mock, when, any
from hamcrest import assert_that
from pyherc.test.matchers import does_have_item, does_not_have_item
from pyherc.test.builders import CharacterBuilder, LevelBuilder, ItemBuilder
from pyherc.test.builders import ActionFactoryBuilder

import satin

from PyQt4.QtTest import QTest
from PyQt4.QtGui import QApplication, QPixmap
from PyQt4.QtCore import Qt

class TestInventoryDialog(object):
    """
    Tests for inventory dialog
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestInventoryDialog, self).__init__()
        self.application = None
        self.action_factory = None
        self.level = None
        self.character = None
        self.surface_manager = None

    def setup(self):
        """
        Setup test case
        """
        self.application = QApplication([])
        self.surface_manager = mock(SurfaceManager)
        when(self.surface_manager).get_icon(any()).thenReturn(QPixmap())

        self.action_factory = (ActionFactoryBuilder()
                                    .with_inventory_factory()
                                    .build())
        self.level = (LevelBuilder()
                            .build())
        self.character = (CharacterBuilder()
                                .with_level(self.level)
                                .with_location((5, 5))
                                .build())

    def teardown(self):
        """
        Tear down the test case
        """
        self.application = None

    def test_picking_up_item(self):
        """
        Test that item can be picked up
        """
        item = (ItemBuilder()
                    .with_name('dagger')
                    .build())
        self.level.add_item(item, (5, 5))

        dialog = InventoryDialog(surface_manager = self.surface_manager,
                                 character = self.character,
                                 action_factory = self.action_factory,
                                 parent = None,
                                 flags = Qt.Dialog)

        QTest.mouseClick(satin.widget(dialog,
                                      slot_with_item('dagger')),
                         Qt.LeftButton)

        assert_that(self.level, does_not_have_item(item.name))

    def test_dropping_item(self):
        """
        Test that item can be dropped
        """
        item = (ItemBuilder()
                    .with_name('dagger')
                    .build())

        self.character.inventory.append(item)

        dialog = InventoryDialog(surface_manager = self.surface_manager,
                                 character = self.character,
                                 action_factory = self.action_factory,
                                 parent = None,
                                 flags = Qt.Dialog)

        QTest.mouseClick(satin.widget(dialog,
                                      slot_with_item('dagger')),
                         Qt.RightButton)

        assert_that(self.level, does_have_item(item.name))

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

"""
Module for testing inventory widget
"""
from herculeum.ui.gui.inventory import InventoryWidget

from herculeum.ui.gui.startgame import StartGameWidget
from pyherc.generators import CreatureConfiguration, CreatureGenerator
from herculeum.ui.gui import QtControlsConfiguration, QtSurfaceManager
from pyherc.test.builders import CharacterBuilder, ActionFactoryBuilder
from pyherc.test.builders import LevelBuilder, ItemBuilder

from PyQt4.QtTest import QTest
from PyQt4.QtGui import QApplication, QPixmap
from PyQt4.QtCore import Qt

from mockito import mock, when, any, verify
from hamcrest import assert_that, is_not, contains  #pylint: disable-msg=E0611
from satin import has_label, satin_suite, all_widgets, widget
from herculeum.test.matchers import slot_with_item
from random import Random

from PyQt4.QtCore import SIGNAL, Qt, QFile
import time

@satin_suite
class TestInventory():
    """
    Tests for inventory widget
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestInventory, self).__init__()

    def setup(self):
        """
        Setup
        """
        self.surface_manager = mock(QtSurfaceManager)
        when(self.surface_manager).get_icon(any()).thenReturn(QPixmap())

        self.level = LevelBuilder().build()

        self.character = (CharacterBuilder()
                        .with_body(5)
                        .with_finesse(6)
                        .with_mind(7)
                        .with_level(self.level)
                        .with_location((5, 5))
                        .build())

        self.item = (ItemBuilder()
                    .with_name('dagger')
                    .build())

        self.level.add_creature(self.character, (5, 5))

        self.action_factory = (ActionFactoryBuilder()
                                    .with_inventory_factory()
                                    .build())

        self.config = QtControlsConfiguration()

    def test_pick_up_item(self):
        """
        Simple test
        """
        self.level.add_item(self.item, (5, 5))
        widget = InventoryWidget(self.surface_manager,
                                 self.character,
                                 self.action_factory,
                                 self.config,
                                 None)

        widget.show()

        QTest.keyClick(widget.items_carried,
                       Qt.Key_Right)

        QTest.keyClick(widget.items_carried,
                       Qt.Key_Left)

        for i in range(6):
            QTest.keyClick(widget.items_carried,
                           Qt.Key_Down)
        QTest.keyClick(widget.items_in_ground,
                       Qt.Key_Space)

        assert_that(self.level.items, is_not(contains(self.item)))
        assert_that(self.character.inventory, contains(self.item))

    def test_drop_item(self):
        """
        Simple test
        """
        self.character.inventory.append(self.item)
        widget = InventoryWidget(self.surface_manager,
                                 self.character,
                                 self.action_factory,
                                 self.config,
                                 None)
        widget.show()

        QTest.keyClick(widget.items_carried,
                       Qt.Key_Right)

        QTest.keyClick(widget.items_carried,
                       Qt.Key_Left)

        QTest.keyClick(widget.items_carried,
                       Qt.Key_Control)

        assert_that(self.level.items, contains(self.item))
        assert_that(self.character.inventory, is_not(contains(self.item)))

    def teardown(self):
        """
        Teardown
        """
        pass

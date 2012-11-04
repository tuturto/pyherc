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
Module for testing list view
"""

from herculeum.gui.surfaceManager import SurfaceManager
from herculeum.gui.widgets import ListViewItem
import herculeum.gui.resources

from mockito import mock, when, any
from hamcrest import assert_that

from satin import has_label

from PyQt4.QtTest import QTest
from PyQt4.QtGui import QApplication, QPixmap
from PyQt4.QtCore import Qt

class TestListViewItem(object):
    """
    Tests for list view item
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestListViewItem, self).__init__()
        self.application = None

    def setup(self):
        """
        Setup test case
        """
        self.application = QApplication([])
        self.surface_manager = mock(SurfaceManager)
        when(self.surface_manager).get_icon(any()).thenReturn(QPixmap())

    def teardown(self):
        """
        Tear down the test case
        """
        self.application = None

    def test_construction_sets_values(self):
        """
        When ListViewItem is constructed, it should show values displayed
        """
        icon = self.surface_manager.get_icon(100)

        item = ListViewItem(title = 'Title',
                            description = 'Here is description',
                            icon = icon)

        assert_that(item, has_label('Title'))
        assert_that(item, has_label('Here is description'))

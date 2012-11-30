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
Package for start screen tests
"""
from herculeum.gui.startgame import StartGameWidget
from pyherc.generators import CreatureConfiguration
from herculeum.gui.surfaceManager import SurfaceManager

from PyQt4.QtTest import QTest
from PyQt4.QtGui import QApplication, QPixmap
from PyQt4.QtCore import Qt

from mockito import mock, when, any
from hamcrest import assert_that
from satin import has_label
from random import Random

class TestStartScreen(object):
    """
    Tests for start screen
    """

    def __init__(self):
        """
        Default constructor
        """
        super(TestStartScreen, self).__init__()
        self.application = None
        self.surface_manager = None

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

    def test_showing_single_character(self):
        """
        Test that a single character can be shown on dialog
        """
        config = {}

        config['Warrior'] = CreatureConfiguration(
                                name = 'Warrior',
                                body = 8,
                                finesse = 8,
                                mind = 5,
                                hp = 9,
                                speed = 1,
                                icons = 101,
                                attack = 1,
                                description = 'Stout warrior')

        dialog = StartGameWidget(config = config,
                                 parent = None,
                                 application = mock(),
                                 surface_manager = self.surface_manager,
                                 flags = Qt.Dialog)

        assert_that(dialog, has_label('Warrior'))
        assert_that(dialog, has_label('Stout warrior'))

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
Package for start screen tests
"""
from herculeum.ui.gui.startgame import StartGameWidget
from pyherc.generators import CreatureConfiguration, CreatureGenerator
from herculeum.ui.gui import QtControlsConfiguration, QtSurfaceManager

from PyQt4.QtTest import QTest
from PyQt4.QtGui import QApplication, QPixmap
from PyQt4.QtCore import Qt

from mockito import mock, when, any, verify
from hamcrest import assert_that #pylint: disable-msg=E0611
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
        self.controls_config = None

    def setup(self):
        """
        Setup test case
        """
        self.application = QApplication([])
        self.surface_manager = mock(QtSurfaceManager)
        when(self.surface_manager).get_icon(any()).thenReturn(QPixmap())

        self.controls_config = QtControlsConfiguration()

        config = {}

        config['Adventurer'] = CreatureConfiguration(
                                    name = 'Adventurer',
                                    body = 8,
                                    finesse = 8,
                                    mind = 5,
                                    hp = 9,
                                    speed = 1,
                                    icons = 101,
                                    attack = 1,
                                    description = 'Clever adventurer')

        config['Thief'] = CreatureConfiguration(
                                    name = 'Thief',
                                    body = 8,
                                    finesse = 8,
                                    mind = 5,
                                    hp = 9,
                                    speed = 1,
                                    icons = 101,
                                    attack = 1,
                                    description = 'Sly thief')

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

        self.generator = mock(CreatureGenerator)
        self.generator.configuration = config

        self.dialog = StartGameWidget(generator = self.generator,
                                      parent = None,
                                      application = mock(),
                                      config = self.controls_config,
                                      surface_manager = self.surface_manager,
                                      flags = Qt.Dialog)

    def teardown(self):
        """
        Tear down the test case
        """
        self.application = None

    def test_showing_character(self):
        """
        Test that a character can be shown on dialog
        """
        assert_that(self.dialog, has_label('Adventurer'))
        assert_that(self.dialog, has_label('Clever adventurer'))

    def test_switching_to_next_character(self):
        """
        Test that next character can be shown
        """
        QTest.keyClick(self.dialog,
                       Qt.Key_6)

        assert_that(self.dialog, has_label('Thief'))
        assert_that(self.dialog, has_label('Sly thief'))

    def test_switching_to_previous_character(self):
        """
        Test that previous character can be shown
        """
        QTest.keyClick(self.dialog,
                       Qt.Key_6)
        QTest.keyClick(self.dialog,
                       Qt.Key_4)

        assert_that(self.dialog, has_label('Adventurer'))
        assert_that(self.dialog, has_label('Clever adventurer'))

    def test_selecting_previous_from_first(self):
        """
        Selecting previous class while at the first, should display the last one
        """
        QTest.keyClick(self.dialog,
                       Qt.Key_4)

        assert_that(self.dialog, has_label('Warrior'))
        assert_that(self.dialog, has_label('Stout warrior'))

    def test_selecting_next_from_last(self):
        """
        Selecting next while at last, should display first
        """
        QTest.keyClick(self.dialog,
                       Qt.Key_6)
        QTest.keyClick(self.dialog,
                       Qt.Key_6)
        QTest.keyClick(self.dialog,
                       Qt.Key_6)
        assert_that(self.dialog, has_label('Adventurer'))
        assert_that(self.dialog, has_label('Clever adventurer'))

    def test_pressing_random_key_does_not_crash_dialog(self):
        """
        Pressing random key should not crash the dialog
        """
        QTest.keyClick(self.dialog,
                       Qt.Key_A)

    def test_generating_character(self):
        """
        Pressing space should trigger character generation
        """
        QTest.keyClick(self.dialog,
                       Qt.Key_Space)

        verify(self.generator).generate_creature(name = 'Adventurer')

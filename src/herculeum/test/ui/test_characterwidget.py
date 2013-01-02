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
Module for testing character widget
"""
from PyQt4.QtGui import QApplication, QPixmap
from pyherc.test.builders import CharacterBuilder, EffectBuilder
from herculeum.gui.character import CharacterWidget

from mockito import mock, when, any
from hamcrest import assert_that
from satin import has_label

class TestCharacterWidget(object):
    """
    Tests for character widget
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestCharacterWidget, self).__init__()
        self.application = None

    def setup(self):
        """
        Setup test case
        """
        self.application = QApplication([])

    def teardown(self):
        """
        Tear down the test case
        """
        self.application = None

    def test_displaying_character(self):
        """
        Displaying character should show stats
        """
        character = (CharacterBuilder()
                        .with_body(5)
                        .with_finesse(6)
                        .with_mind(7)
                        .build())

        surface_manager = mock()
        when(surface_manager).get_icon(any()).thenReturn(QPixmap())

        widget = CharacterWidget(surface_manager = surface_manager,
                                 character = character,
                                 parent = None)

        assert_that(widget, has_label(str(character.body)))
        assert_that(widget, has_label(str(character.finesse)))
        assert_that(widget, has_label(str(character.mind)))

    def test_displaying_effects(self):
        """
        Displaying character should show effects
        """
        character = (CharacterBuilder()
                        .with_body(5)
                        .with_finesse(6)
                        .with_mind(7)
                        .with_effect(EffectBuilder()
                                        .with_title('Cure minor wounds')
                                        .with_description('Cures small amount of damage')
                                        )
                        .build())

        surface_manager = mock()
        when(surface_manager).get_icon(any()).thenReturn(QPixmap())

        widget = CharacterWidget(surface_manager = surface_manager,
                                 character = character,
                                 parent = None)

        assert_that(widget, has_label('Cure minor wounds'))
        assert_that(widget, has_label('Cures small amount of damage'))

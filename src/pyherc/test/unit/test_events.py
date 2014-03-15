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
Tests for events
"""
from pyherc.test.builders import CharacterBuilder

from mockito import mock, verify


class TestCharacterEvents():
    """
    Tests for Character's event handling
    """
    def __init__(self):
        super().__init__()

    def test_that_character_relays_events(self):
        """
        Test that events relayed to the character are relayed forward
        """
        listener = mock()
        event = mock()

        character = (CharacterBuilder()
                     .with_event_listener(listener)
                     .build())

        character.receive_event(event)

        verify(listener).receive_event(event)

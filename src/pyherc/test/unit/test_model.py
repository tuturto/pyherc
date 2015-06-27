# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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
Module for testing Model
"""
#pylint: disable=W0614
from hamcrest import assert_that  # pylint: disable-msg=E0611
from mockito import mock, verify
from pyherc.data import Model
from pyherc.events import MoveEvent
from pyherc.test.builders import CharacterBuilder, LevelBuilder
from pyherc.test.matchers import has_event_listener


class TestModel():
    """
    Class for testing Model
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestModel, self).__init__()

        self.model = None
        self.listener = None
        self.level = None

    def setup(self):
        """
        Setup test cases
        """
        self.model = Model()
        self.listener = mock()
        self.level = LevelBuilder().build()

        self.model.register_event_listener(self.listener)

    def test_registering_event_listener(self):
        """
        Test that event listener can be registered on the model
        """
        assert_that(self.model, has_event_listener(self.listener))

    def test_dispatching_event_to_listeners(self):
        """
        Test that events are dispatched to listeners
        """
        event = MoveEvent(mover = (CharacterBuilder()
                                        .with_model(self.model)
                                        .build()),
                          affected_tiles = [],
                          old_location = (5, 5),
                          old_level = self.level,
                          direction = 1)

        self.model.raise_event(event)

        verify(self.listener).receive_event(event)

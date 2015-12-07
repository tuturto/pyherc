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
Module for testing Model
"""
#pylint: disable=W0614
from hamcrest import assert_that  # pylint: disable-msg=E0611
from mockito import mock, verify
from pyherc.data import Model
from pyherc.events import new_move_event
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
        event = new_move_event(character = (CharacterBuilder()
                                        .with_model(self.model)
                                        .build()),
                               old_location = (5, 5),
                               old_level = self.level,
                               direction = 1)

        self.model.raise_event(event)

        verify(self.listener).receive_event(event)

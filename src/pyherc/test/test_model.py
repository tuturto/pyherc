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
Module for testing Model
"""
#pylint: disable=W0614
from pyherc.data import Model
from pyherc.test.matchers import has_event_listener
from hamcrest import * #pylint: disable=W0401
from mockito import mock

class TestModel(object):
    """
    Class for testing Model
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestModel, self).__init__()

    def test_registering_event_listener(self):
        """
        Test that event listener can be registered on the model
        """
        model = Model()

        listener = mock()

        model.register_event_listener(listener)

        assert_that(model, has_event_listener(listener))

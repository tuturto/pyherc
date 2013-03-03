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
Module for testing effects collection
"""
#pylint: disable=W0614
from pyherc.data.effects import EffectsCollection
from pyherc.test.builders import EffectHandleBuilder
from pyherc.test.builders import EffectBuilder
from hamcrest import assert_that, is_in, is_not, is_, equal_to #pylint: disable-msg=E0611
from pyherc.test.matchers import has_effect_handle, has_effect_handles
from pyherc.test.matchers import has_effect

class TestEffectsCollection(object):
    """
    Class to test effects collection
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestEffectsCollection, self).__init__()
        self.collection = None

    def setup(self):
        """
        Setup test case
        """
        self.collection = EffectsCollection()

    def test_adding_effect_handle(self):
        """
        Test that effect handle can be added and retrieved
        """
        handle = EffectHandleBuilder().build()

        self.collection.add_effect_handle(handle)

        assert_that(self.collection, has_effect_handle(handle))

    def test_adding_multiple_handles(self):
        """
        Test that adding two handles don't create key collisions
        """
        handle1 = (EffectHandleBuilder()
                        .with_effect('heal')
                        .build())
        handle2 = (EffectHandleBuilder()
                        .with_effect('bless')
                        .build())

        self.collection.add_effect_handle(handle1)
        self.collection.add_effect_handle(handle2)

        assert_that(self.collection, has_effect_handles([handle1, handle2]))

    def test_returning_only_specific_handles(self):
        """
        Test that handles can be retrieved by their trigger
        """
        handle1 = (EffectHandleBuilder()
                        .with_trigger('on drink')
                        .build())
        handle2 = (EffectHandleBuilder()
                        .with_trigger('on bash')
                        .build())
        self.collection.add_effect_handle(handle1)
        self.collection.add_effect_handle(handle2)

        handles = self.collection.get_effect_handles('on bash')

        assert_that(handle2, is_in(handles))

    def test_no_matching_trigger(self):
        """
        Test that collection returns an empty list when trigger does not match
        """
        handle1 = (EffectHandleBuilder()
                        .with_trigger('on sleep')
                        .build())
        self.collection.add_effect_handle(handle1)

        handles = self.collection.get_effect_handles('on kick')

        assert_that(handles, is_(equal_to([])))

    def test_removing_handle(self):
        """
        Test that a handle can be removed
        """
        handle = EffectHandleBuilder().build()

        self.collection.add_effect_handle(handle)
        self.collection.remove_effect_handle(handle)

        assert_that(self.collection, is_not(has_effect_handle(handle)))

    def test_adding_effects(self):
        """
        Test that an effect can be added
        """
        effect = EffectBuilder().build()

        self.collection.add_effect(effect)

        assert_that(self.collection, has_effect(effect))

    def test_removing_expired_effects(self):
        """
        Test that expired effects are removed
        """
        effect = (EffectBuilder()
                    .with_duration(0)
                    .build())

        self.collection.add_effect(effect)
        self.collection.remove_expired_effects()

        assert_that(self.collection, is_not(has_effect(effect)))

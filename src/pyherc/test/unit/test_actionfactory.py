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
Module for testing combat related rules
"""

from hamcrest import assert_that, contains_inanyorder, is_, is_in, same_instance
from mockito import any, mock, when
from pyherc.data.model import Model
from pyherc.rules.combat.factories import AttackFactory
from pyherc.rules.combat.interface import AttackParameters
from pyherc.rules.moving.factories import MoveFactory
from pyherc.rules.public import ActionFactory


class TestActionFactories():
    """
    Tests related to action factories
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_init_single_factory(self):
        """
        Test that action factory can be initialised with single sub factory
        """
        mock_model = mock(Model)
        mock_attack_factory = AttackFactory([])

        factory = ActionFactory(mock_model,
                                mock_attack_factory)

        factories = factory.get_sub_factories()
        assert_that(mock_attack_factory, is_in(factories))

    def test_init_factory_list(self):
        """
        Test that action factory can be initialised with list of factories
        """
        mock_model = mock(Model)
        mock_move_factory = mock(MoveFactory)
        mock_attack_factory = mock(AttackFactory)

        factory = ActionFactory(mock_model,
                                [mock_attack_factory,
                                    mock_move_factory])
        factories = factory.get_sub_factories()

        assert_that(factories, contains_inanyorder(mock_attack_factory,
                                                   mock_move_factory))

    def test_get_factory_by_type(self):
        """
        Test that factory can be found by using Parameters object
        """
        mock_model = mock(Model)
        mock_move_factory = mock(MoveFactory)
        mock_attack_factory = mock(AttackFactory)

        when(mock_attack_factory).can_handle(any()).thenReturn(True)
        when(mock_move_factory).can_handle(any()).thenReturn(False)

        factory = ActionFactory(mock_model,
                                [mock_attack_factory,
                                 mock_move_factory])

        mock_parameters = mock(AttackParameters)

        sub_factory = factory.get_sub_factory(mock_parameters)

        assert_that(sub_factory, is_(same_instance(mock_attack_factory)))

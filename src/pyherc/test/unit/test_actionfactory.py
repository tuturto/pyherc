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
Module for testing combat related rules
"""
#pylint: disable=W0614
from pyherc.rules.public import ActionFactory
from pyherc.rules.public import AttackParameters
from pyherc.rules.attack.factories import AttackFactory
from pyherc.rules.move.factories import MoveFactory
from pyherc.data.model import Model
from mockito import mock, when, any
from hamcrest import * #pylint: disable=W0401

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
        mock_attack_factory = mock(AttackFactory)

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

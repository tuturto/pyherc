#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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

'''
Module for testing combat related rules
'''

import random
from pyherc.test import IntegrationTest
from pyherc.test import StubModel
from pyherc.rules.public import ActionFactory
from pyherc.rules.public import AttackParameters
from pyherc.rules.attack.factories import AttackFactory
from pyherc.rules.attack.factories import UnarmedCombatFactory
from pyherc.rules.move.factories import MoveFactory
from pyherc.rules.move.factories import WalkFactory
from pyherc.rules.attack.action import AttackAction
from pyherc.data.model import Character
from pyherc.data.dungeon import Level
from pyherc.data import tiles

from pyherc.data.model import Model

from mock import Mock

class TestActionFactories():
    '''
    Tests related to action factories
    '''
    def test_init_single_factory(self):
        '''
        Test that action factory can be initialised with single sub factory
        '''
        mock_model = Mock(Model)
        mock_attack_factory = Mock(AttackFactory)

        factory = ActionFactory(mock_model,
                                mock_attack_factory)

        factories = factory.get_sub_factories()
        found = [isinstance(x, AttackFactory) for x in factories]
        assert True in found

    def test_init_factory_list(self):
        '''
        Test that action factory can be initialised with list of factories
        '''
        mock_model = Mock(Model)
        mock_move_factory = Mock(MoveFactory)
        mock_attack_factory = Mock(AttackFactory)

        factory = ActionFactory(mock_model,
                                [mock_attack_factory,
                                    mock_move_factory])
        factories = factory.get_sub_factories()

        found = [isinstance(x, AttackFactory) for x in factories]
        assert True in found

        found = [isinstance(x, MoveFactory) for x in factories]
        assert True in found

    def test_get_factory_by_type(self):
        '''
        Test that factory can be found by using Parameters object
        '''
        mock_model = Mock(Model)
        mock_move_factory = Mock(MoveFactory)
        mock_attack_factory = Mock(AttackFactory)

        mock_attack_factory.can_handle.return_value = True
        mock_move_factory.can_handle.return_value = False

        factory = ActionFactory(mock_model,
                                [mock_attack_factory,
                                    mock_move_factory])

        mock_parameters = Mock(AttackParameters)

        sub_factory = factory.get_sub_factory(mock_parameters)

        assert isinstance(sub_factory, AttackFactory)

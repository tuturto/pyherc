#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

'''
Module for testing combat related rules
'''

import random
from pyHerc.test import IntegrationTest
from pyHerc.test import StubModel
from pyHerc.rules.public import ActionFactory
from pyHerc.rules.public import AttackParameters
from pyHerc.rules.attack.factories import AttackFactory
from pyHerc.rules.attack.factories import UnarmedCombatFactory
from pyHerc.rules.move.factories import MoveFactory
from pyHerc.rules.move.factories import WalkFactory
from pyHerc.rules.attack.action import AttackAction
from pyHerc.data.model import Character
from pyHerc.data.dungeon import Level
from pyHerc.data import tiles

from pyHerc.data.model import Model

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

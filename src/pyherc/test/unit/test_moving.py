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
Module for testing moving
"""
#pylint: disable=W0614
from hamcrest import * #pylint: disable=W0401
from mockito import mock

from pyherc.rules import MoveParameters
from pyherc.rules.move.action import EscapeAction
from pyherc.data import Portal
from pyherc.test.builders import LevelBuilder
from pyherc.test.builders import CharacterBuilder

from pyherc.data import Model
from pyherc.data.model import ESCAPED_DUNGEON
from pyherc.test.builders import ActionFactoryBuilder
from pyherc.test.helpers import EventListener
from pyherc.test.matchers import has_marked_for_redrawing

import pyherc.rules.moving

class TestEventDispatching(object):
    """
    Tests for event dispatching relating to moving
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestEventDispatching, self).__init__()

        self.model = None
        self.character = None
        self.action_factory = None
        self.level = None
        self.listener = None

    def setup(self):
        """
        Setup test case
        """
        self.model = Model()

        self.action_factory = (ActionFactoryBuilder()
                                    .with_move_factory()
                                    .build())

        self.character = (CharacterBuilder()
                                .with_model(self.model)
                                .with_location((10, 10))
                                .build())

        self.level = (LevelBuilder()
                            .with_character(self.character)
                            .build())

        self.listener = EventListener()

        self.model.register_event_listener(self.listener)

    def test_event_is_relayed(self):
        """
        Test that moving will create an event and send it forward
        """
        self.character.move(3,
                            self.action_factory)

        assert_that(len(self.listener.events), is_(equal_to(1)))

    def test_affected_tiles_are_marked(self):
        """
        Test that moving marks tiles for redrawing
        """
        expected_redraws = [(10, 10),
                            (10, 11)]

        self.character.move(5,
                            self.action_factory)

        event = self.listener.events[0]

        assert_that(event, has_marked_for_redrawing(expected_redraws))

class TestMoving(object):
    """
    Tests for moving
    """

    def __init__(self):
        """
        Default constructor
        """
        super(TestMoving, self).__init__()
        self.action_factory = None
        self.character = None
        self.level1 = None
        self.level2 = None
        self.portal1 = None
        self.portal2 = None
        self.model = None

    def setup(self):
        """
        Setup the test case
        """
        self.action_factory = ActionFactoryBuilder().with_move_factory().build()

        self.character = (CharacterBuilder()
                                .build())

        self.level1 = (LevelBuilder()
                            .with_wall_at((1, 0))
                            .build())

        self.level2 = LevelBuilder().build()
        self.portal1 = Portal((None, None), None)

        self.portal1.icon = 1
        self.portal2 = Portal((None, None), None)
        self.portal2 = Portal((None, None), None)

        self.level1.add_portal(self.portal1, (5, 5))
        self.level2.add_portal(self.portal2, (10, 10), self.portal1)

        self.level1.add_creature(self.character, (5, 5))

    def test_simple_move(self):
        """
        Test that taking single step is possible
        """
        self.character.location = (5, 5)

        self.character.move(3,
                            self.action_factory)

        assert_that(self.character.location,
                    is_(equal_to((6, 5))))

    def test_walking_to_walls(self):
        """
        Test that it is not possible to walk through walls
        """
        self.character.location = (1, 1)

        self.character.move(1,
                            self.action_factory)

        assert(self.character.location == (1, 1))

    def test_entering_portal(self):
        """
        Test that character can change level via portal
        """
        assert(self.character.location == (5, 5))
        assert(self.character.level == self.level1)

        self.character.move(9,
                            self.action_factory)

        assert(self.character.location == (10, 10))
        assert(self.character.level == self.level2)

    def test_entering_portal_adds_character_to_creatures(self):
        """
        Test that entering portal will add character to the creatures list
        """
        assert self.character.level == self.level1
        assert self.character in self.level1.creatures

        self.character.move(9,
                            self.action_factory)

        assert self.character.level == self.level2
        assert self.character in self.level2.creatures

    def test_entering_portal_removes_character_from_old_level(self):
        """
        Test that entering portal will remove character from level
        """
        assert self.character.level == self.level1
        assert self.character in self.level1.creatures

        self.character.move(9,
                            self.action_factory)

        assert self.character not in self.level1.creatures

    def test_entering_non_existent_portal(self):
        """
        Test that character can not walk through floor
        """
        self.character.location = (6, 3)
        assert(self.character.level == self.level1)

        self.character.move(9,
                            self.action_factory)

        assert(self.character.location == (6, 3))
        assert(self.character.level == self.level1)

    def test_moving_uses_time(self):
        """
        Test that moving around uses time
        """
        tick = self.character.tick

        self.character.move(3,
                            self.action_factory)

        assert self.character.tick > tick

    def test_taking_escape_stairs_ends_game(self):
        """
        Test that player taking escape stairs will create escape
        """
        portal3 = Portal((None, None), None)
        portal3.exits_dungeon = True
        self.level1.add_portal(portal3, (2, 2))
        self.character.location = (2, 2)

        self.character.move(direction = 9,
                            action_factory = self.action_factory)

        model = self.character.model
        assert_that(model.end_condition, is_(equal_to(ESCAPED_DUNGEON)))

class TestEscapeAction(object):
    """
    Tests for escape action
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestEscapeAction, self).__init__()

    def test_player_character_can_escape(self):
        """
        Test that escape action for player character is legal
        """
        model = mock()

        character = (CharacterBuilder()
                        .as_player_character()
                        .with_model(model)
                        .build())

        action = EscapeAction(character = character)

        assert_that(action.is_legal(), is_(equal_to(True)))

    def test_non_player_character_can_not_escape(self):
        """
        Non player characters should not be able to escape
        """
        model = mock()

        character = (CharacterBuilder()
                        .with_model(model)
                        .build())

        action = EscapeAction(character = character)

        assert_that(action.is_legal(), is_(equal_to(False)))

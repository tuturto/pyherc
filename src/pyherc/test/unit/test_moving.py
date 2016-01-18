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
Module for testing moving
"""

from hamcrest import assert_that, equal_to, is_
from mockito import mock
from pyherc.data import (Model, Portal, add_portal, add_character, get_characters,
                         get_character)
from pyherc.data.constants import Direction
from pyherc.data.model import ESCAPED_DUNGEON
from pyherc.ports import is_move_legal, move, set_action_factory
from pyherc.rules.moving.action import EscapeAction
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  LevelBuilder)
from pyherc.test.helpers import EventListener
from pyherc.test.matchers import has_marked_for_redrawing, is_illegal, is_legal, EventType
from mockito import verify, mock


class TestEventDispatching():
    """
    Tests for event dispatching relating to moving
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.model = None
        self.character = None
        self.level = None
        self.listener = None
        self.actions = None

    def setup(self):
        """
        Setup test case
        """
        self.model = Model()

        self.character = (CharacterBuilder()
                          .with_model(self.model)
                          .with_location((1, 1))
                          .build())

        self.model.dungeon = (LevelBuilder()
                              .with_character(self.character)
                              .build())

        self.listener = mock()

        self.model.register_event_listener(self.listener)

        set_action_factory(ActionFactoryBuilder()
                           .with_move_factory()
                           .build())

    def test_event_is_relayed(self):
        """
        Test that moving will create an event and send it forward
        """
        move(character=self.character,
             direction=Direction.east)

        verify(self.listener).receive_event(EventType('move'))


class TestMoving():
    """
    Tests for moving
    """

    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.actions = None
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
        self.character = (CharacterBuilder()
                          .build())

        self.level1 = (LevelBuilder()
                       .with_floor_tile("floor")
                       .with_wall_at((1, 0))
                       .build())

        self.level2 = (LevelBuilder()
                       .with_floor_tile("floor")
                       .build())
        self.portal1 = Portal((None, None), None)

        self.portal1.icon = 1
        self.portal2 = Portal(("stairs", "stairs"), None)
        self.portal2 = Portal(("stairs", "stairs"), None)

        add_portal(self.level1, (5, 5), self.portal1)
        add_portal(self.level2, (10, 10), self.portal2, self.portal1)

        add_character(self.level1, (5, 5), self.character)

        set_action_factory(ActionFactoryBuilder()
                           .with_move_factory()
                           .build())

    def test_moving_when_stairs_are_blocked(self):
        """
        Moving should be possible, even if stairs other end is blocked
        """
        blocker = CharacterBuilder().build()

        add_character(self.level2, (10, 10), blocker)

        move(character=self.character,
             direction=Direction.enter)

        assert_that(blocker.level, is_(equal_to(self.level2)))
        assert_that(self.character.level, is_(equal_to(self.level2)))

    def check_move_result(self, start, direction, expected_location):
        """
        Test that taking single step is possible
        """
        self.character.location = start

        move(character=self.character,
             direction=direction)

        assert_that(self.character.location,
                    is_(equal_to(expected_location)))

    def test_simple_move(self):
        """
        Test that taking single step is possible
        """
        test_data = [(1, (5, 4)),
                     (2, (6, 4)),
                     (3, (6, 5)),
                     (4, (6, 6)),
                     (5, (5, 6)),
                     (6, (4, 6)),
                     (7, (4, 5)),
                     (8, (4, 4))]

        for row in test_data:
            yield (self.check_move_result, (5, 5), row[0], row[1])

    def test_walking_to_walls(self):
        """
        Test that it is not possible to walk through walls
        """
        self.character.location = (1, 1)

        move(character=self.character,
             direction=Direction.north)

        assert_that(self.character.location, is_(equal_to((1, 1))))

    def test_entering_portal(self):
        """
        Test that character can change level via portal
        """
        move(character=self.character,
             direction=Direction.enter)

        assert_that(self.character.level, is_(equal_to(self.level2)))
        assert_that(self.character.location, is_(equal_to((10, 10))))

    def test_entering_portal_adds_character_to_creatures(self):
        """
        Test that entering portal will add character to the creatures list
        """
        assert self.character.level == self.level1
        assert self.character in get_characters(self.level1)

        move(character=self.character,
             direction=Direction.enter)

        assert self.character.level == self.level2
        assert self.character in get_characters(self.level2)

    def test_entering_portal_removes_character_from_old_level(self):
        """
        Test that entering portal will remove character from level
        """
        assert self.character.level == self.level1
        assert self.character in get_characters(self.level1)

        move(character=self.character,
             direction=Direction.enter)

        assert self.character not in get_characters(self.level1)

    def test_entering_non_existent_portal(self):
        """
        Test that character can not walk through floor
        """
        self.character.location = (6, 3)

        move(character=self.character,
             direction=Direction.enter)

        assert_that(self.character.location, is_(equal_to((6, 3))))
        assert_that(self.character.level, is_(equal_to(self.level1)))

    def test_moving_uses_time(self):
        """
        Test that moving around uses time
        """
        tick = self.character.tick

        move(character=self.character,
             direction=Direction.east)

        assert self.character.tick > tick

    def test_taking_escape_stairs_ends_game(self):
        """
        Test that player taking escape stairs will create escape
        """
        portal3 = Portal((None, None), None)
        portal3.exits_dungeon = True
        add_portal(self.level1, (2, 2), portal3)
        self.character.location = (2, 2)

        move(character=self.character,
             direction=Direction.enter)

        model = self.character.model
        assert_that(model.end_condition, is_(equal_to(ESCAPED_DUNGEON)))


class TestEscapeAction():
    """
    Tests for escape action
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_player_character_can_escape(self):
        """
        Test that escape action for player character is legal
        """
        model = mock()

        character = (CharacterBuilder()
                     .as_player_character()
                     .with_model(model)
                     .build())

        action = EscapeAction(character=character)

        assert_that(action, is_legal())

    def test_non_player_character_can_not_escape(self):
        """
        Non player characters should not be able to escape
        """
        model = mock()

        character = (CharacterBuilder()
                     .with_model(model)
                     .build())

        action = EscapeAction(character=character)

        assert_that(action, is_illegal())


class TestSwitchingPlaces():
    """
    Sometimes characters can switch places with each other
    """

    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.level = None
        self.monster_1 = None
        self.monster_2 = None
        self.actions = None

    def setup(self):
        """
        Test setup
        """
        self.level = LevelBuilder().build()

        self.monster_1 = (CharacterBuilder()
                          .with_name('Pete')
                          .build())

        self.monster_2 = (CharacterBuilder()
                          .with_name('Uglak')
                          .build())

        self.monster_1.artificial_intelligence = lambda : None
        self.monster_2.artificial_intelligence = lambda : None

        add_character(self.level, (5, 5), self.monster_1)
        add_character(self.level, (6, 5), self.monster_2)

        set_action_factory(ActionFactoryBuilder()
                           .with_move_factory()
                           .build())

    def test_switch_places(self):
        """
        Two monsters can switch places
        """
        move(self.monster_1, Direction.east)

        assert_that(self.monster_1.location, is_(equal_to((6, 5))))
        assert_that(self.monster_2.location, is_(equal_to((5, 5))))

    def test_system_consistency(self):
        """
        Switching places should leave system in consistent state
        """
        move(self.monster_1, Direction.east)

        assert_that(get_character(self.level, (6, 5)), is_(equal_to(self.monster_1)))
        assert_that(get_character(self.level, (5, 5)), is_(equal_to(self.monster_2)))

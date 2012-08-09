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
Tests for gui components
"""
#pylint: disable=W0614
from mockito import mock
from hamcrest import * #pylint: disable=W0401

from pygame import Rect

import herculeum.gui.windows
from pyherc.data import Model
from herculeum.gui.surfaceManager import SurfaceManager
from herculeum.gui.gamewindow import GameArea
from herculeum.application import Application
from pyherc.events import MoveEvent
from pyherc.test.builders import CharacterBuilder
from pyherc.test.builders import LevelBuilder
from pyherc.test.builders import ActionFactoryBuilder

class TestGameWindow(object):
    """
    Tests for main game window
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestGameWindow, self).__init__()

    def test_updating_screen_while_monster_moves(self):
        """
        Test that only needed spots are reported as updated as a monster moves
        """
        model = Model()
        surface = mock()

        player = (CharacterBuilder()
                        .with_model(model)
                        .as_player_character()
                        .with_name('player')
                        .with_location((11, 11))
                        .build())

        action_factory = (ActionFactoryBuilder()
                                .with_model(model)
                                .with_move_factory()
                                .build())

        monster = (CharacterBuilder()
                        .with_model(model)
                        .with_name('rat')
                        .with_location((5, 5))
                        .build())

        level = (LevelBuilder()
                    .with_character(player)
                    .with_character(monster)
                    .build())

        application = Application()
        application.world = model

        game_gui = GameArea(application = application,
                            surface_manager = mock(),
                            action_factory = mock(),
                            decorate = False,
                            width = 800,
                            height = 600)

        game_gui.old_location = player.location

        model.register_event_listener(game_gui)

        game_gui.paint(surface)
        monster.move(7,
                     action_factory)
        rects = game_gui.update(surface)

        assert_that(rects, has_items(Rect(160, 88, 192, 120),
                                     Rect(192, 88, 224, 120)))

    def test_player_moving_updates_whole_screen(self):
        """
        Test that moving player character reports whole screen updated
        """
        model = Model()
        surface = mock()

        action_factory = (ActionFactoryBuilder()
                                .with_model(model)
                                .with_move_factory()
                                .build())

        player = (CharacterBuilder()
                        .with_model(model)
                        .as_player_character()
                        .with_name('player')
                        .with_location((11, 11))
                        .build())

        monster = (CharacterBuilder()
                        .with_model(model)
                        .with_name('rat')
                        .with_location((5, 5))
                        .build())

        level = (LevelBuilder()
                    .with_character(player)
                    .with_character(monster)
                    .build())

        application = Application()
        application.world = model

        game_gui = GameArea(application = application,
                            surface_manager = mock(),
                            action_factory = mock(),
                            decorate = False,
                            width = 800,
                            height = 600)

        game_gui.old_location = player.location

        model.register_event_listener(game_gui)

        player.move(7,
                    action_factory)
        rects = game_gui.update(surface)

        assert_that(rects, has_items(Rect(0, 0, 800, 600)))

    def test_recording_dirty_tiles(self):
        """
        Test that GameArea records dirty tiles for updating based on events
        """
        level = LevelBuilder().build()

        game_gui = GameArea(application = Application(),
                            surface_manager = mock(),
                            action_factory = mock(),
                            decorate = False)

        tiles = [(10, 10),
                 (11, 11)]

        mover = mock()
        mover.location = (10, 10)
        mover.level = mock()

        game_gui.receive_event(MoveEvent(mover = mover,
                                         affected_tiles = tiles))

        assert_that(game_gui.dirty_tiles, has_items((10, 10), (11, 11)))

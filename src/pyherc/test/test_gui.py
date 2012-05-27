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

"""
Tests for gui components
"""
#pylint: disable=W0614
from mockito import mock
from hamcrest import * #pylint: disable=W0401

from pygame import Rect

import pyherc.gui.windows
from pyherc.data import Character
from pyherc.data import Model
from pyherc.gui.surfaceManager import SurfaceManager
from pyherc.test import IntegrationTest
from pyherc.gui.gamewindow import GameArea
from pyherc.application import Application
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

        monster = (CharacterBuilder()
                        .with_model(model)
                        .with_action_factory(ActionFactoryBuilder()
                                                .with_model(model)
                                                .with_move_factory())
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
                            decorate = False)

        game_gui.old_location = player.location

        model.register_event_listener(game_gui)

        monster.move(7)
        rects = game_gui.update(surface)

        assert_that(rects, has_items(Rect(160, 88, 192, 120),
                                     Rect(192, 88, 224, 120)))

    def test_recording_dirty_tiles(self):
        """
        Test that GameArea records dirty tiles for updating based on events
        """
        level = LevelBuilder().build()

        game_gui = GameArea(application = Application(),
                            surface_manager = mock(),
                            decorate = False)

        tiles = [(10, 10),
                 (11, 11)]

        game_gui.receive_event(MoveEvent(level = level,
                                         location = (10, 10),
                                         affected_tiles = tiles))

        assert_that(game_gui.dirty_tiles, has_items((10, 10), (11, 11)))

    def test_formatting_event_history_less_than_five_items(self):
        """
        Test that event history is formatted correctly with less than five items
        """
        window = pyherc.gui.windows.OldGameWindow(mock(),
                                                  mock(),
                                                  mock())
        window.eventHistory = []
        window.eventHistory.append('one')
        window.eventHistory.append('two')
        result = window.format_event_history()
        assert(result[0] == 'one')
        assert(result[1] == 'two')

    def test_formatting_event_history_five_items(self):
        """
        Test that event history is formatted correctly with five items
        """
        window = pyherc.gui.windows.OldGameWindow(mock(),
                                                  mock(),
                                                  mock())
        window.eventHistory = []
        window.eventHistory.append('one')
        window.eventHistory.append('two')
        window.eventHistory.append('three')
        window.eventHistory.append('four')
        window.eventHistory.append('five')
        result = window.format_event_history()
        assert(result[0] == 'one')
        assert(result[1] == 'two')
        assert(result[2] == 'three')
        assert(result[3] == 'four')
        assert(result[4] == 'five')

    def test_formatting_event_history_more_than_five_items(self):
        """
        Test that event history is formatted correctly with more than five items
        """
        window = pyherc.gui.windows.OldGameWindow(mock(),
                                                  mock(),
                                                  mock())
        window.eventHistory = []
        window.eventHistory.append('one')
        window.eventHistory.append('two')
        window.eventHistory.append('three')
        window.eventHistory.append('four')
        window.eventHistory.append('five')
        window.eventHistory.append('six')
        result = window.format_event_history()
        print result
        assert(len(result) == 5)
        assert(result[0] == 'two')
        assert(result[1] == 'three')
        assert(result[2] == 'four')
        assert(result[3] == 'five')
        assert(result[4] == 'six')

class TestInventoryDialog(IntegrationTest):
    """
    Tests for Inventory dialog
    """
    def __init__(self):
        """
        Default constructor
        """
        IntegrationTest.__init__(self)

    def test_sort_items(self):
        """
        Test that items can be sorted by their type
        """
        mock_surface_manager = mock(SurfaceManager)
        mock_character = mock(Character)
        inventory = pyherc.gui.dialogs.Inventory(None,
                                                 None,
                                                 mock_surface_manager,
                                                 mock_character)

        item1 = self.item_generator.generate_item({'name': 'dagger'})
        item2 = self.item_generator.generate_item({'name': 'apple'})
        item3 = self.item_generator.generate_item({'name': 'healing potion'})
        item4 = self.item_generator.generate_item({'name': 'short sword'})
        item5 = self.item_generator.generate_item({'name': 'minor potion of poison'})
        item6 = self.item_generator.generate_item({'name': 'longspear'})
        item7 = self.item_generator.generate_item({'name': 'apple'})
        item8 = self.item_generator.generate_item({'name': 'minor healing potion'})

        unsorted = [item1, item2, item3, item4, item5, item6, item7, item8]

        sorted = inventory.sort_items(unsorted)

        assert len(sorted) == 8
        assert sorted[0].get_main_type() == 'weapon'
        assert sorted[1].get_main_type() == 'weapon'
        assert sorted[2].get_main_type() == 'weapon'
        assert sorted[3].get_main_type() == 'potion'
        assert sorted[4].get_main_type() == 'potion'
        assert sorted[5].get_main_type() == 'potion'
        assert sorted[6].get_main_type() == 'food'
        assert sorted[7].get_main_type() == 'food'

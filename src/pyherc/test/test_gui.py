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
Tests for gui components
'''
from pyDoubles.framework import stub #pylint: disable=F0401, E0611

import pyherc.gui.windows
from pyherc.data import Character
from pyherc.gui.surfaceManager import SurfaceManager
from pyherc.test import IntegrationTest


class TestGameWindow:
    '''
    Tests for main game window
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def test_formatting_event_history_less_than_five_items(self):
        '''
        Test that event history is formatted correctly with less than five items
        '''
        window = pyherc.gui.windows.GameWindow(None, None, '')
        window.eventHistory = []
        window.eventHistory.append('one')
        window.eventHistory.append('two')
        result = window.formatEventHistory()
        assert(result[0] == 'one')
        assert(result[1] == 'two')

    def test_formatting_event_history_five_items(self):
        '''
        Test that event history is formatted correctly with five items
        '''
        window = pyherc.gui.windows.GameWindow(None, None, '')
        window.eventHistory = []
        window.eventHistory.append('one')
        window.eventHistory.append('two')
        window.eventHistory.append('three')
        window.eventHistory.append('four')
        window.eventHistory.append('five')
        result = window.formatEventHistory()
        assert(result[0] == 'one')
        assert(result[1] == 'two')
        assert(result[2] == 'three')
        assert(result[3] == 'four')
        assert(result[4] == 'five')

    def test_formatting_event_history_more_than_five_items(self):
        '''
        Test that event history is formatted correctly with more than five items
        '''
        window = pyherc.gui.windows.GameWindow(None, None, '')
        window.eventHistory = []
        window.eventHistory.append('one')
        window.eventHistory.append('two')
        window.eventHistory.append('three')
        window.eventHistory.append('four')
        window.eventHistory.append('five')
        window.eventHistory.append('six')
        result = window.formatEventHistory()
        print result
        assert(len(result) == 5)
        assert(result[0] == 'two')
        assert(result[1] == 'three')
        assert(result[2] == 'four')
        assert(result[3] == 'five')
        assert(result[4] == 'six')

class TestInventoryDialog(IntegrationTest):
    '''
    Tests for Inventory dialog
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        IntegrationTest.__init__(self)

    def test_sort_items(self):
        '''
        Test that items can be sorted by their type
        '''
        mock_surface_manager = stub(SurfaceManager)
        mock_character = stub(Character)
        inventory = pyherc.gui.dialogs.Inventory(None,
                                                        None,
                                                        mock_surface_manager,
                                                        mock_character)

        item1 = self.item_generator.generateItem(self.tables, {'name': 'dagger'})
        item2 = self.item_generator.generateItem(self.tables, {'name': 'apple'})
        item3 = self.item_generator.generateItem(self.tables, {'name': 'healing potion'})
        item4 = self.item_generator.generateItem(self.tables, {'name': 'short sword'})
        item5 = self.item_generator.generateItem(self.tables, {'name': 'minor potion of poison'})
        item6 = self.item_generator.generateItem(self.tables, {'name': 'longspear'})
        item7 = self.item_generator.generateItem(self.tables, {'name': 'apple'})
        item8 = self.item_generator.generateItem(self.tables, {'name': 'minor healing potion'})

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


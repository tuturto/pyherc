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
#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

"""
Module for testing creatures
"""

from pyherc.data.model import Character, WeaponProficiency
from pyherc.test import IntegrationTest
from pyherc.generators.level.testlevel import TestLevelGenerator
from pyherc.data.dungeon import Dungeon
from pyherc.rules.moving import deactivate
from pyherc.data.item import Item


class test_CreatureWithGenerator(IntegrationTest):
    """
    Tests for creatures that require generators to be working
    """
    def __init__(self):
        '''
        Default constructor
        '''
        IntegrationTest.__init__(self)

    def test_rat_generation(self):
        """
        Test that generating a rat is possible
        """
        creature = self.creatureGenerator.generate_creature({
                                                'name': 'rat'})

        assert(creature.name == 'rat')

    def test_is_proficient(self):
        '''
        Test that weapon proficiency of character can be checked
        '''
        creature = Character(self.action_factory)
        creature.feats = []

        weapon = self.item_generator.generate_item(self.tables, {'name' : 'club'})

        assert(creature.is_proficient(weapon) == False)

        creature.feats.append(WeaponProficiency('simple'))

        assert(creature.is_proficient(weapon) == True)

class TestStatues(IntegrationTest):
    '''
    Test handling of statues (mainly mimicing items)
    '''

    def __init__(self):
        '''
        Default constructor
        '''
        IntegrationTest.__init__(self)

    def test_deactivating_creature(self):
        '''
        Test that activated character can deactivate
        '''
        creature = Character(self.action_factory)
        creature.name = 'Mimic'
        item = Item()

        item.name = 'Chest'

        creature.set_mimic_item(item)

        levelGenerator = TestLevelGenerator(self.action_factory,
                                            self.creatureGenerator,
                                            self.item_generator)

        self.model.dungeon = Dungeon()
        self.level1 = levelGenerator.generate_level(None, self.model, monster_list = [])

        self.model.dungeon.levels = self.level1

        self.level1.add_creature(creature, self.level1.find_free_space())

        location = creature.location

        assert self.level1.get_creature_at(location) == creature
        assert len(self.level1.get_items_at(location)) == 0

        deactivate(self.model, creature)

        assert self.level1.get_creature_at(location) == None
        assert len(self.level1.get_items_at(location)) == 1

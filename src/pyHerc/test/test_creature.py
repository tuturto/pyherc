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

#import pyHerc
#import pyHerc.generators.item
#import pyHerc.data.tiles
#import pyHerc.data.dungeon
#import pyHerc.rules.items
#import pyHerc.rules.tables
from pyHerc.data.model import Character, WeaponProficiency
from pyHerc.test import IntegrationTest

class test_CreatureWithGenerator(IntegrationTest):
    """
    Tests for creatures that require generators to be working
    """

    def test_rat_generation(self):
        """
        Test that generating a rat is possible
        """
        creature = self.creatureGenerator.generate_creature(self.tables, {
                                                'name': 'rat'})

        assert(creature.name == 'rat')

    def test_is_proficient(self):
        '''
        Test that weapon proficiency of character can be checked
        '''
        creature = Character()
        creature.feats = []

        weapon = self.itemGenerator.generateItem(self.tables, {'name' : 'club'})

        assert(creature.is_proficient(weapon) == False)

        creature.feats.append(WeaponProficiency('simple'))

        assert(creature.is_proficient(weapon) == True)

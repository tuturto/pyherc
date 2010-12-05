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

import os, sys
import logging
import pyHerc
import pyHerc.data.model
from pyHerc.data import tiles

class Tables:

    def __init__(self):
        self.__initialised = 0
        # all items, name as key
        self.items = {}
        # item names, sorted by tags
        self.itemsByTag = {}
        self.tagScore = {}

        self.creatures = {}
        self.sizeModifier = []
        self.attributeModifier = []

    def loadTables(self):
        """
        Initialise tables
        """
        artifact = 1
        legendary = 2
        epic = 4
        rare = 8
        uncommon = 16
        common = 32

        if self.__initialised:
            return

        self.items['apple'] = {'name' : 'apple',
                                    'cost' : 1,
                                    'weight' : 1,
                                    'icon' : pyHerc.data.tiles.item_apple,
                                    'type' : ['food'],
                                    'rarity' : common}

        self.items['crystal skull'] = {'name' : 'Crystal skull',
                                                            'questItem' : 1,
                                                            'icon' : pyHerc.data.tiles.item_crystal_skull,
                                                            'type' : ['special item', 'quest item'],
                                                            'rarity' : artifact}

        self.items['dagger'] = {'name' : 'dagger',
                                            'cost' : 2,
                                            'damage' : '1d4',
                                            'critical range' : 19,
                                            'critical damage' : 2,
                                            'weight' : 1,
                                            'damage type' : ['piercing', 'slashing'],
                                            'class' : 'simple',
                                            'icon' : [pyHerc.data.tiles.item_dagger_1,
                                                            pyHerc.data.tiles.item_dagger_2],
                                            'type' : ['weapon', 'light weapon', 'melee', 'simple weapon'],
                                            'rarity' : common}

        self.items['morning star'] = {'name' : 'morning star',
                                                    'cost' : 8,
                                                    'damage' : '1d8',
                                                    'critical range' : 20,
                                                    'critical damage' : 2,
                                                    'weight' : 6,
                                                    'damage type' : ['bludgeoning', 'piercing'],
                                                    'class' : 'simple',
                                                    'icon' : [pyHerc.data.tiles.item_morning_star_1,
                                                                    pyHerc.data.tiles.item_morning_star_2],
                                                    'type' : ['weapon', 'one-handed weapon', 'melee', 'simple weapon'],
                                                    'rarity' : common}

        self.items['short sword'] = {'name' : 'short sword',
                                                'cost' : 10,
                                                'damage' : '1d6',
                                                'critical range' : 19,
                                                'critical damage' : 2,
                                                'weight' : 2,
                                                'damage type' : ['piercing'],
                                                'class' : 'martial',
                                                'icon' : [pyHerc.data.tiles.item_short_sword_1,
                                                                pyHerc.data.tiles.item_short_sword_2],
                                                'type' : ['weapon', 'light weapon', 'melee', 'martial weapon'],
                                                'rarity' : common}

        self.creatures['rat'] = {'name' : 'rat',
                                        'str' : 4,
                                        'dex' : 12,
                                        'con' : 4,
                                        'int' : 2,
                                        'wis' : 4,
                                        'cha' : 4,
                                        'hp' : 2,
                                        'speed' : 2,
                                        'icon' : [pyHerc.data.tiles.creature_rat_1,
                                                        pyHerc.data.tiles.creature_rat_2,
                                                        pyHerc.data.tiles.creature_rat_3,
                                                        pyHerc.data.tiles.creature_rat_4],
                                        'attack' : '1d4',
                                        'size' : 'small'}

        self.sizeModifier = {'colossal' :  -8, 'gargantuan' : -4, 'huge' : -2, 'large' : -1,
                                'medium' : 0, 'small' : 1, 'tiny' : 2, 'diminutive' : 4, 'fine' : 8}

        self.attributeModifier = [-6, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

        self.__constructLookupTables()

    def __constructLookupTables(self):
        """
        Construct lookup tables for different kinds of items
        """

        self.itemsByTag = {}
        self.tagScore = {}

        for itemKey in self.items.keys():
            for type in self.items[itemKey]['type']:
                if type in self.itemsByTag.keys():
                    lowerBound = self.tagScore[type]
                    self.tagScore[type] = self.tagScore[type] + self.items[itemKey]['rarity']
                    upperBound = self.tagScore[type]
                    self.itemsByTag[type].append((itemKey, lowerBound, upperBound))
                else:
                    self.itemsByTag[type] = []
                    lowerBound = 0
                    self.tagScore[type] = self.items[itemKey]['rarity']
                    upperBound = self.tagScore[type]
                    self.itemsByTag[type].append((itemKey, lowerBound, upperBound))

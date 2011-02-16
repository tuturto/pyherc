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

import os, sys, StringIO
import logging
import pyHerc
import pyHerc.data.model
from pyHerc.data import tiles
from xml import sax

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

    def readItemsFromXML(self, document):
        parser = sax.make_parser()
        handler = ItemHandler()
        parser.setContentHandler(handler)
        file = StringIO.StringIO(document)
        parser.parse(file)
        self.items = handler.items

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
                                                            'cost' : 0,
                                                            'weight' : 5,
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
                                            'icon' : [pyHerc.data.tiles.item_dagger_1],
                                            'type' : ['weapon', 'light weapon', 'melee', 'simple weapon'],
                                            'rarity' : common}

        self.items['light mace'] = {'name' : 'light mace',
                                            'cost' : 5,
                                            'damage' : '1d6',
                                            'critical range' : 20,
                                            'critical damage' : 2,
                                            'weight' : 4,
                                            'damage type' : ['bludgeoning'],
                                            'class' : 'simple',
                                            'icon' : [pyHerc.data.tiles.item_light_mace],
                                            'type' : ['weapon', 'light weapon', 'melee', 'simple weapon'],
                                            'rarity' : common}

        self.items['sickle'] = {'name' : 'sickle',
                                            'cost' : 6,
                                            'damage' : '1d6',
                                            'critical range' : 20,
                                            'critical damage' : 2,
                                            'weight' : 2,
                                            'damage type' : ['slashing'],
                                            'class' : 'simple',
                                            'icon' : [pyHerc.data.tiles.item_sickle],
                                            'type' : ['weapon', 'light weapon', 'melee', 'simple weapon'],
                                            'rarity' : common}

        self.items['club'] = {'name' : 'club',
                                            'cost' : 0,
                                            'damage' : '1d6',
                                            'critical range' : 20,
                                            'critical damage' : 2,
                                            'weight' : 3,
                                            'damage type' : ['bludgeoning'],
                                            'class' : 'simple',
                                            'icon' : [pyHerc.data.tiles.item_club],
                                            'type' : ['weapon', 'one-handed weapon', 'melee', 'simple weapon'],
                                            'rarity' : common}

        self.items['heavy mace'] = {'name' : 'heavy mace',
                                            'cost' : 12,
                                            'damage' : '1d8',
                                            'critical range' : 20,
                                            'critical damage' : 2,
                                            'weight' : 8,
                                            'damage type' : ['bludgeoning'],
                                            'class' : 'simple',
                                            'icon' : [pyHerc.data.tiles.item_mace],
                                            'type' : ['weapon', 'one-handed weapon', 'melee', 'simple weapon'],
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

        self.items['shortspear'] = {'name' : 'shortspear',
                                                    'cost' : 1,
                                                    'damage' : '1d6',
                                                    'critical range' : 20,
                                                    'critical damage' : 2,
                                                    'weight' : 3,
                                                    'damage type' : ['piercing'],
                                                    'class' : 'simple',
                                                    'icon' : [pyHerc.data.tiles.item_shortspear],
                                                    'type' : ['weapon', 'one-handed weapon', 'melee', 'simple weapon'],
                                                    'rarity' : common}

        self.items['longspear'] = {'name' : 'longspear',
                                                    'cost' : 5,
                                                    'damage' : '1d8',
                                                    'critical range' : 20,
                                                    'critical damage' : 3,
                                                    'weight' : 9,
                                                    'damage type' : ['piercing'],
                                                    'class' : 'simple',
                                                    'icon' : [pyHerc.data.tiles.item_longspear],
                                                    'type' : ['weapon', 'two-handed weapon', 'melee', 'simple weapon'],
                                                    'rarity' : common}

#       self.items['quarterstaff'] = {'name' : 'quarterstaff',
#                                                    'cost' : 0,
#                                                    'damage' : '1d6/1d6',
#                                                    'critical range' : 20,
#                                                    'critical damage' : 2,
#                                                    'weight' : 4,
#                                                    'damage type' : ['bludgeoning'],
#                                                    'class' : 'simple',
#                                                    'icon' : [pyHerc.data.tiles.item_quarterstaff],
#                                                    'type' : ['weapon', 'two-handed weapon', 'melee', 'simple weapon'],
#                                                    'rarity' : common}

        self.items['spear'] = {'name' : 'spear',
                                                    'cost' : 2,
                                                    'damage' : '1d8',
                                                    'critical range' : 20,
                                                    'critical damage' : 3,
                                                    'weight' : 6,
                                                    'damage type' : ['piercing'],
                                                    'class' : 'simple',
                                                    'icon' : [pyHerc.data.tiles.item_spear],
                                                    'type' : ['weapon', 'two-handed weapon', 'melee', 'simple weapon'],
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

        self.creatures['fire beetle'] = {'name' : 'fire beetle',
                                        'str' : 10,
                                        'dex' : 11,
                                        'con' : 11,
                                        'int' : 0,
                                        'wis' : 10,
                                        'cha' : 7,
                                        'hp' : 4,
                                        'speed' : 1.9,
                                        'icon' : [pyHerc.data.tiles.creature_beetle_1,
                                                        pyHerc.data.tiles.creature_beetle_2],
                                        'attack' : '2d4',
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


class ItemHandler(sax.ContentHandler):
    """
    Class to process items xml-configuration
    """
    def startElement(self, name, attrs):
        self.text = ""
        if name == 'items':
            #start of the configuration document
            self.items = {}
        elif name == 'item':
            #start of new item
            self.newItem = {}
        elif name == 'types':
            #start of types section
            self.newItem['type'] = []

    def characters(self, ch):
        self.text = self.text + ch

    def endElement(self, name):
        if name == 'items':
            #finished processing the items configuration
            pass
        elif name == 'item':
            #finished processing item
            self.items[self.newItem['name']] = self.newItem
            self.newItem = None
        elif name == 'name':
            #finished processing name node
            self.newItem['name'] = self.text
        elif name == 'cost':
            self.newItem['cost'] = int(self.text)
        elif name == 'weight':
            self.newItem['weight'] = int(self.text)
        elif name == 'type':
            self.newItem['type'].append(self.text)
        elif name == 'rarity':
            self.newItem['rarity'] = self.text
        elif name == 'icon':
            #TODO: for now, until better way is discovered
            self.newItem['icon'] = int(self.text)


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

        self.artifact = 1
        self.legendary = 2
        self.epic = 4
        self.rare = 8
        self.uncommon = 16
        self.common = 32

    def readItemsFromXML(self, document):
        parser = sax.make_parser()
        handler = ItemHandler()
        parser.setContentHandler(handler)
        file = StringIO.StringIO(document)
        parser.parse(file)
        self.items = handler.items

    def loadTables(self, itemConfig = None):
        """
        Initialise tables
        @param itemConfig: optional config string for items
        """

        if self.__initialised:
            return

        if itemConfig != None:
            #use passed config
            self.readItemsFromXML(itemConfig)
        else:
            #open file and read from there
            #TODO: relative location
            f = open('C:/programming/pyHack/resources/items.xml', 'r')
            itemConfig = f.read()
            f.close()
            self.readItemsFromXML(itemConfig)

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
        elif name == 'damageTypes':
            self.newItem['damage type'] = []
        elif name == 'icons':
            self.newItem['icon'] = []

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
            #TODO: for now, until better way is found
            if self.text == 'artifact':
                self.newItem['rarity'] = 1
            elif self.text == 'legendary':
                self.newItem['rarity'] = 2
            elif self.text == 'epic':
                self.newItem['rarity'] = 4
            elif self.text == 'rare':
                self.newItem['rarity'] = 8
            elif self.text == 'uncommon':
                self.newItem['rarity'] = 16
            elif self.text == 'common':
                self.newItem['rarity'] = 32
        elif name == 'icon':
            self.newItem['icon'].append(pyHerc.data.tiles.__dict__[self.text])
        elif name == 'questItem':
            self.newItem['questItem'] = int(self.text)
        elif name == 'damage':
            self.newItem['damage'] = self.text
        elif name == 'criticalRange':
            self.newItem['critical range'] = int(self.text)
        elif name == 'criticalDamage':
            self.newItem['critical damage'] = int(self.text)
        elif name == 'damageType':
            self.newItem['damage type'].append(self.text)
        elif name == 'class':
            self.newItem['class'] = self.text


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

import os, sys, StringIO, random
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

        self.__logger = logging.getLogger('pyHerc.rules.tables')

    def readItemsFromXML(self, document):
        self.__logger.debug('reading item config from xml')
        parser = sax.make_parser()
        handler = ItemHandler()
        parser.setContentHandler(handler)
        file = StringIO.StringIO(document)
        parser.parse(file)
        self.items = handler.items
        self.__logger.debug('item config read from xml')

    def readCreaturesFromXML(self, document):
        self.__logger.debug('reading creature config from xml')
        parser = sax.make_parser()
        handler = CreatureHandler()
        parser.setContentHandler(handler)
        file = StringIO.StringIO(document)
        parser.parse(file)
        self.creatures = handler.creatures
        self.__logger.debug('creature config read from xml')

    def loadTables(self, itemConfig = None, creatureConfig = None):
        """
        Initialise tables
        @param itemConfig: optional config string for items
        @param creatureConfig: optional config string for creatures
        """

        if self.__initialised:
            return

        self.__logger.debug('loading tables')

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

        if creatureConfig != None:
            #use passed config
            self.readCreaturesFromXML(creatureConfig)
        else:
            #open file and read from there
            #TODO: relative location
            f = open('C:/programming/pyHack/resources/creatures.xml', 'r')
            creatureConfig = f.read()
            f.close()
            self.readCreaturesFromXML(creatureConfig)

        self.sizeModifier = {'colossal' :  -8, 'gargantuan' : -4, 'huge' : -2, 'large' : -1,
                                'medium' : 0, 'small' : 1, 'tiny' : 2, 'diminutive' : 4, 'fine' : 8}

        self.attributeModifier = [-6, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

        self.potionAppearances = [
                                ('clay potion',  pyHerc.data.tiles.item_potion_3),
                                ('ruby potion', pyHerc.data.tiles.item_potion_9),
                                ('yellow potion', pyHerc.data.tiles.item_potion_10),
                                ('dark green potion', pyHerc.data.tiles.item_potion_2),
                                ('cyan potion',  pyHerc.data.tiles.item_potion_4),
                                ('sky blue potion', pyHerc.data.tiles.item_potion_5),
                                ('bubbly potion', pyHerc.data.tiles.item_potion_8),
                                ('black potion', pyHerc.data.tiles.item_potion_6),
                                ('brown potion', pyHerc.data.tiles.item_potion_1),
                                ('brown potion', pyHerc.data.tiles.item_potion_7),
                                ('black potion', pyHerc.data.tiles.item_potion_11),
                                ('brilliant blue potion', pyHerc.data.tiles.item_potion_12),
                                ('milky potion', pyHerc.data.tiles.item_potion_13),
                                ('amber potion', pyHerc.data.tiles.item_potion_14),
                                ('pink potion', pyHerc.data.tiles.item_potion_15),
                                ('swirly potion', pyHerc.data.tiles.item_potion_16),
                                ('dark blue potion', pyHerc.data.tiles.item_potion_17),
                                ('murky potion', pyHerc.data.tiles.item_potion_18),
                                ('red potion', pyHerc.data.tiles.item_potion_19),
                                ('golden potion', pyHerc.data.tiles.item_potion_20),
                                ('emerald potion', pyHerc.data.tiles.item_potion_21),
                                ('fizzy potion', pyHerc.data.tiles.item_potion_22),
                                ('silver potion', pyHerc.data.tiles.item_potion_23),
                                ('smoky potion', pyHerc.data.tiles.item_potion_24)
                                ]

        self.constructLookupTables()
        self.randomizePotions()

    def randomizePotions(self):
        """
        Randomize appearances of potions
        @note: different types of potions may be assigned same appearance
        """
        self.__logger.debug('randomizing potion appearance')
        potionEntries = self.itemsByTag['potion']
        for entry in potionEntries:
            appearance = random.choice(self.potionAppearances)
            self.items[entry[0]]['appearance'] = appearance[0]
            self.items[entry[0]]['icon'] = [appearance[1]]
        self.__logger.debug('potion appearance randomized')

    def constructLookupTables(self):
        """
        Construct lookup tables for different kinds of items
        """
        self.__logger.debug('constructing look up tables')
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

        self.__logger.debug('look up tables constructed')

class CreatureHandler(sax.ContentHandler):
    """
    Class to read creatures from xml-configuration
    """
    def startElement(self, name, attrs):
        self.text = ""
        if name == 'creatures':
            #start of the configuration document
            self.creatures = {}
        elif name == 'creature':
            #start of new item
            self.newCreature = {}
        elif name == 'icons':
            self.newCreature['icon'] = []

    def characters(self, ch):
        self.text = self.text + ch

    def endElement(self, name):
        if name == 'creature':
            #finished processing creature
            self.creatures[self.newCreature['name']] = self.newCreature
            self.newCreature = None
        elif name in ('name', 'size', 'attack'):
            self.newCreature[name] = self.text
        elif name in ('str', 'dex', 'con', 'int', 'wis', 'cha', 'hp'):
            self.newCreature[name] = int(self.text)
        elif name == 'speed':
            self.newCreature['speed'] = float(self.text)
        elif name == 'icon':
            self.newCreature['icon'].append(pyHerc.data.tiles.__dict__[self.text])

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
        elif name == 'effects':
            self.newItem['effects'] = {}
        elif name == 'effect':
            #new effect
            tempEffect = {}
            effectType = attrs['type']
            if 'name' in attrs.keys():
                tempEffect['name'] = attrs['name']
            if 'power' in attrs.keys():
                tempEffect['power'] = attrs['power']

            if not effectType in self.newItem['effects'].keys():
                self.newItem['effects'][effectType] = []

            self.newItem['effects'][effectType].append(tempEffect)

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
        elif name == 'charges':
            self.newItem['charges'] = int(self.text)


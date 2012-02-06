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

import os, StringIO, random, os.path
import logging
import pyherc
import pyherc.data.model
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
        self.potion_appearances = []

        self.artifact = 1
        self.legendary = 2
        self.epic = 4
        self.rare = 8
        self.uncommon = 16
        self.common = 32

        self.logger = logging.getLogger('pyherc.rules.tables')

    def __getstate__(self):
        '''
        Override __getstate__ in order to get pickling work
        '''
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        '''
        Override __setstate__ in order to get pickling work
        '''
        self.__dict__.update(d)
        self.logger = logging.getLogger('pyherc.rules.tables')

    def read_items_from_xml(self, document):
        self.logger.debug('reading item config from xml')
        parser = sax.make_parser()
        handler = ItemHandler()
        parser.setContentHandler(handler)
        file = StringIO.StringIO(document)
        parser.parse(file)
        self.items = handler.items
        self.logger.debug('item config read from xml')

    def read_creatures_from_xml(self, document):
        self.logger.debug('reading creature config from xml')
        parser = sax.make_parser()
        handler = CreatureHandler()
        parser.setContentHandler(handler)
        file = StringIO.StringIO(document)
        parser.parse(file)
        self.creatures = handler.creatures
        self.logger.debug('creature config read from xml')

    def load_tables(self, base_path = None, itemConfig = None, creatureConfig = None):
        """
        Initialise tables
        @param base_path: directory from where to load files
        @param itemConfig: optional config string for items
        @param creatureConfig: optional config string for creatures
        """

        if self.__initialised:
            return

        self.logger.debug('loading tables')

        if itemConfig != None:
            #use passed config
            self.read_items_from_xml(itemConfig)
        else:
            #open file and read from there
            f = open(os.path.join(base_path, 'items.xml'), 'r')
            itemConfig = f.read()
            f.close()
            self.read_items_from_xml(itemConfig)

        if creatureConfig != None:
            #use passed config
            self.read_creatures_from_xml(creatureConfig)
        else:
            #open file and read from there
            f = open(os.path.join(base_path, 'creatures.xml'), 'r')
            creatureConfig = f.read()
            f.close()
            self.read_creatures_from_xml(creatureConfig)

        self.potion_appearances = [
                                ('clay potion',  pyherc.data.tiles.ITEM_POTION_3),
                                ('ruby potion', pyherc.data.tiles.ITEM_POTION_9),
                                ('yellow potion', pyherc.data.tiles.ITEM_POTION_10),
                                ('dark green potion', pyherc.data.tiles.ITEM_POTION_2),
                                ('cyan potion',  pyherc.data.tiles.ITEM_POTION_4),
                                ('sky blue potion', pyherc.data.tiles.ITEM_POTION_5),
                                ('bubbly potion', pyherc.data.tiles.ITEM_POTION_8),
                                ('black potion', pyherc.data.tiles.ITEM_POTION_6),
                                ('brown potion', pyherc.data.tiles.ITEM_POTION_1),
                                ('brown potion', pyherc.data.tiles.ITEM_POTION_7),
                                ('black potion', pyherc.data.tiles.ITEM_POTION_11),
                                ('brilliant blue potion', pyherc.data.tiles.ITEM_POTION_12),
                                ('milky potion', pyherc.data.tiles.ITEM_POTION_13),
                                ('amber potion', pyherc.data.tiles.ITEM_POTION_14),
                                ('pink potion', pyherc.data.tiles.ITEM_POTION_15),
                                ('swirly potion', pyherc.data.tiles.ITEM_POTION_16),
                                ('dark blue potion', pyherc.data.tiles.ITEM_POTION_17),
                                ('murky potion', pyherc.data.tiles.ITEM_POTION_18),
                                ('red potion', pyherc.data.tiles.ITEM_POTION_19),
                                ('golden potion', pyherc.data.tiles.ITEM_POTION_20),
                                ('emerald potion', pyherc.data.tiles.ITEM_POTION_21),
                                ('fizzy potion', pyherc.data.tiles.ITEM_POTION_22),
                                ('silver potion', pyherc.data.tiles.ITEM_POTION_23),
                                ('smoky potion', pyherc.data.tiles.ITEM_POTION_24)
                                ]

        self.construct_lookup_tables()
        self.randomise_potions()

    def randomise_potions(self):
        """
        Randomize appearances of potions
        @note: different types of potions may be assigned same appearance
        """
        self.logger.debug('randomizing potion appearance')
        potionEntries = self.itemsByTag['potion']
        for entry in potionEntries:
            appearance = random.choice(self.potion_appearances)
            self.items[entry[0]]['appearance'] = appearance[0]
            self.items[entry[0]]['icon'] = [appearance[1]]
        self.logger.debug('potion appearance randomized')

    def construct_lookup_tables(self):
        """
        Construct lookup tables for different kinds of items
        """
        self.logger.debug('constructing look up tables')
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

        self.logger.debug('look up tables constructed')

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
        elif name in ('attack'):
            self.newCreature[name] = int(self.text)
        elif name in ('name', 'size'):
            self.newCreature[name] = self.text
        elif name in ('body', 'finesse', 'mind', 'hp'):
            self.newCreature[name] = int(self.text)
        elif name == 'speed':
            self.newCreature['speed'] = float(self.text)
        elif name == 'icon':
            self.newCreature['icon'].append(pyherc.data.tiles.__dict__[self.text])

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
            self.newItem['icon'].append(pyherc.data.tiles.__dict__[self.text])
        elif name == 'questItem':
            self.newItem['questItem'] = int(self.text)
        elif name == 'damage':
            self.newItem['damage'] = int(self.text)
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


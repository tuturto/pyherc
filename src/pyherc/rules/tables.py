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
Module for handling tables
"""

import os, StringIO, random, os.path
import logging
import pyherc
import pyherc.data.model
from xml import sax

class Tables:
    """
    Class representing tables
    """

    def __init__(self):
        """
        Default constructor
        """
        self.__initialised = 0
        # all items, name as key
        self.items = {}
        # item names, sorted by tags
        self.__items_by_tag = {}
        self.__tag_score = {}

        self.__creatures = {}
        self.potion_appearances = []

        self.artifact = 1
        self.legendary = 2
        self.epic = 4
        self.rare = 8
        self.uncommon = 16
        self.common = 32

        self.logger = logging.getLogger('pyherc.rules.tables')

    def __get_tag_score(self):
        """
        Returns tag score
        """
        return self.__tag_score

    def __get_items_by_tag(self):
        """
        Returns items by tag
        """
        return self.__items_by_tag

    tag_score = property(__get_tag_score)
    items_by_tag = property(__get_items_by_tag)

    def __get_creatures(self):
        """
        Get creature tables

        Returns:
            Dictionary of creatures
        """
        return self.__creatures

    creatures = property(__get_creatures)

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(d)
        self.logger = logging.getLogger('pyherc.rules.tables')

    def read_items_from_xml(self, document):
        """
        Read items from supplied xml-document
        """
        self.logger.info('reading item config from xml')
        parser = sax.make_parser()
        handler = ItemHandler()
        parser.setContentHandler(handler)
        file = StringIO.StringIO(document)
        parser.parse(file)
        self.items = handler.items
        self.logger.info('item config read from xml')
        self.logger.info('{0} items found'.
                          format(len(self.items)))

    def read_creatures_from_xml(self, document):
        """
        Read creatures from supplied xml-document
        """
        self.logger.info('reading creature config from xml')
        parser = sax.make_parser()
        handler = CreatureHandler()
        parser.setContentHandler(handler)
        file = StringIO.StringIO(document)
        parser.parse(file)
        self.creatures = handler.creatures
        self.logger.info('creature config read from xml')
        self.logger.info('{0} creatures found'
                          .format(len(self.creatures.keys())))

    def load_tables(self, base_path = None, itemConfig = None, creatureConfig = None):
        """
        Initialise tables

        Args:
            base_path: directory from where to load files
            itemConfig: optional config string for items
            creatureConfig: optional config string for creatures
        """

        if self.__initialised:
            return

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
                                ('dark flask', pyherc.data.tiles.ITEM_POTION_1),
                                ('brown potion', pyherc.data.tiles.ITEM_POTION_2),
                                ('dark green bottle', pyherc.data.tiles.ITEM_POTION_3),
                                ('clay potion', pyherc.data.tiles.ITEM_POTION_4),
                                ('cyan flask', pyherc.data.tiles.ITEM_POTION_5),
                                ('sky blue elixir', pyherc.data.tiles.ITEM_POTION_6),
                                ('bubbling potion', pyherc.data.tiles.ITEM_POTION_7),
                                ('dark potion', pyherc.data.tiles.ITEM_POTION_8),
                                ('earthly potion', pyherc.data.tiles.ITEM_POTION_9),
                                ('earthly bottle', pyherc.data.tiles.ITEM_POTION_10),
                                ('ruby potion', pyherc.data.tiles.ITEM_POTION_11),
                                ('yellow flask', pyherc.data.tiles.ITEM_POTION_12),
                                ('milky bottle', pyherc.data.tiles.ITEM_POTION_13),
                                ('amber potion', pyherc.data.tiles.ITEM_POTION_14),
                                ('amaranth potion', pyherc.data.tiles.ITEM_POTION_15),
                                ('sky blue potion', pyherc.data.tiles.ITEM_POTION_16),
                                ('sky blue bottle', pyherc.data.tiles.ITEM_POTION_17),
                                ('dark green potion', pyherc.data.tiles.ITEM_POTION_18),
                                ('red tinctura', pyherc.data.tiles.ITEM_POTION_19),
                                ('golden potion', pyherc.data.tiles.ITEM_POTION_20),
                                ('emerald flask', pyherc.data.tiles.ITEM_POTION_21),
                                ('emerald bottle', pyherc.data.tiles.ITEM_POTION_22),
                                ('bubbling bottle', pyherc.data.tiles.ITEM_POTION_23),
                                ('bubbling flask', pyherc.data.tiles.ITEM_POTION_24),
                                ('dark tinctura', pyherc.data.tiles.ITEM_POTION_25),
                                ('purple tinctura', pyherc.data.tiles.ITEM_POTION_26),
                                ('light blue bottle', pyherc.data.tiles.ITEM_POTION_27),
                                ('emerald potion', pyherc.data.tiles.ITEM_POTION_28),
                                ('red potion', pyherc.data.tiles.ITEM_POTION_29),
                                ('night flask', pyherc.data.tiles.ITEM_POTION_30),
                                ('red concoction', pyherc.data.tiles.ITEM_POTION_31),
                                ('green concoction', pyherc.data.tiles.ITEM_POTION_32),
                                ('puple concoction', pyherc.data.tiles.ITEM_POTION_33),
                                ('milky flask', pyherc.data.tiles.ITEM_POTION_34),
                                ('fiery potion', pyherc.data.tiles.ITEM_POTION_35),
                                ('fiery bottle', pyherc.data.tiles.ITEM_POTION_36),
                                ('rosy potion', pyherc.data.tiles.ITEM_POTION_37),
                                ('rosy bottle', pyherc.data.tiles.ITEM_POTION_38),
                                ('maroon potion', pyherc.data.tiles.ITEM_POTION_39),
                                ('fuchsia flask', pyherc.data.tiles.ITEM_POTION_40),
                                ('fuchsia potion', pyherc.data.tiles.ITEM_POTION_41),
                                ('crimson potion', pyherc.data.tiles.ITEM_POTION_42),
                                ('crimson flask', pyherc.data.tiles.ITEM_POTION_43),
                                ('swirly potion', pyherc.data.tiles.ITEM_POTION_44),
                                ('clear potion', pyherc.data.tiles.ITEM_POTION_45),
                                ('orange tinctura', pyherc.data.tiles.ITEM_POTION_46),
                                ('fuchsia tinctura', pyherc.data.tiles.ITEM_POTION_47),
                                ('crimson vial', pyherc.data.tiles.ITEM_POTION_48),
                                ('milky potion', pyherc.data.tiles.ITEM_POTION_49),
                                ('yellow tinctura', pyherc.data.tiles.ITEM_POTION_50),
                                ('fuchsia bottle', pyherc.data.tiles.ITEM_POTION_51),
                                ('orange bottle', pyherc.data.tiles.ITEM_POTION_52),
                                ('red mixture', pyherc.data.tiles.ITEM_POTION_53),
                                ('rosy flask', pyherc.data.tiles.ITEM_POTION_54),
                                ('golden flask', pyherc.data.tiles.ITEM_POTION_55),
                                ('dark mixture', pyherc.data.tiles.ITEM_POTION_56),
                                ('golden elixir', pyherc.data.tiles.ITEM_POTION_57),
                                ('lava potion', pyherc.data.tiles.ITEM_POTION_58),
                                ('golden mixture', pyherc.data.tiles.ITEM_POTION_59),
                                ('golden tinctura', pyherc.data.tiles.ITEM_POTION_60)]

        self.construct_lookup_tables()
        self.randomise_potions()

    def randomise_potions(self):
        """
        Randomize appearances of potions

        Note:
            different types of potions may be assigned same appearance
        """
        potionEntries = self.items_by_tag['potion']
        for entry in potionEntries:
            appearance = random.choice(self.potion_appearances)
            self.items[entry[0]]['appearance'] = appearance[0]
            self.items[entry[0]]['icon'] = [appearance[1]]

    def construct_lookup_tables(self):
        """
        Construct lookup tables for different kinds of items
        """
        self.items_by_tag = {}
        self.tag_score = {}

        for itemKey in self.items.keys():
            for type in self.items[itemKey]['type']:
                if type in self.items_by_tag.keys():
                    lowerBound = self.tag_score[type]
                    self.tag_score[type] = self.tag_score[type] + self.items[itemKey]['rarity']
                    upperBound = self.tag_score[type]
                    self.items_by_tag[type].append((itemKey, lowerBound, upperBound))
                else:
                    self.items_by_tag[type] = []
                    lowerBound = 0
                    self.tag_score[type] = self.items[itemKey]['rarity']
                    upperBound = self.tag_score[type]
                    self.items_by_tag[type].append((itemKey, lowerBound, upperBound))

class CreatureHandler(sax.ContentHandler):
    """
    Class to read creatures from xml-configuration
    """
    def startElement(self, name, attrs):
        """
        Handle starting of element
        """
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
        """
        Handle reading character inside element
        """
        self.text = self.text + ch

    def endElement(self, name):
        """
        Handle ending of element
        """
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
        """
        Handle starting of element
        """
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
            if 'charges' in attrs.keys():
                tempEffect['charges'] = int(attrs['charges'])
            else:
                tempEffect['charges'] = 1

            if not effectType in self.newItem['effects'].keys():
                self.newItem['effects'][effectType] = []

            self.newItem['effects'][effectType].append(tempEffect)

    def characters(self, ch):
        """
        Handle reading character inside of element
        """
        self.text = self.text + ch

    def endElement(self, name):
        """
        Handle ending of element
        """
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


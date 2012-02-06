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

import random
import pyherc.data.dungeon
import pyherc.data.model
import pyherc.rules.tables

from pyherc.rules.public import ActionFactory
from pyherc.rules.move.factories import MoveFactory
from pyherc.rules.move.factories import WalkFactory

from pyherc.rules.attack.factories import UnarmedCombatFactory
from pyherc.rules.attack.factories import MeleeCombatFactory
from pyherc.rules.attack.factories import AttackFactory

class StubRandomNumberGenerator(random.Random):
    '''
    Stub for random number generator

    Will always return same numbers
    '''
    def __init__(self):
        self.numbers = []

    def inject(self, max, numbers):
        self.numbers = [(x / max) - 0.0000000000000001 for x in numbers]

    def random(self):
        '''
        Return the next random floating point number in the range [0.0, 1.0).
        '''
        return self.numbers.pop(0)

    def seed(self, seed = None):
        '''
        Initialize the basic random number generator.
        '''
        pass

    def getstate(self):
        '''
        Return an object capturing the current internal state of the generator.
        This object can be passed to setstate() to restore the state.
        '''
        return self.numbers

    def setstate(self, state):
        '''
        state should have been obtained from a previous call to getstate()
        setstate() restores the internal state of the generator to what it was
        at the time setstate() was called.
        '''
        self.numbers = state

    def jumpahead(self, jumps):
        pass


class StubCharacter:
    """
    Stub for Character class
    """
    def __init__(self):
        pass

    def receive_event(self, event):
        pass

    def get_max_hp(self):
        return 10

    def identify_item(self, item):
        pass

    def is_proficient(self, weapon):
        return True

class StubSurfaceManager():
    '''
    Simple stub to act as a surface manager
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def loadResources(self):
        pass

    def getImage(self, id):
        return None

    def getIcon(self, id):
        return None

class StubModel():
    """
    Simple stub to act as model and do nothing
    """
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def raise_event(self, event):
        pass

class IntegrationTest():

    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def setup(self):
        itemConfig = """
<items>
    <item>
        <name>apple</name>
        <cost>1</cost>
        <weight>1</weight>
        <icons>
            <icon>ITEM_APPLE</icon>
        </icons>
        <types>
            <type>food</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>crystal skull</name>
        <cost>0</cost>
        <weight>5</weight>
        <questItem>1</questItem>
        <icons>
            <icon>ITEM_CRYSTAL_SKULL</icon>
        </icons>
        <types>
            <type>special item</type>
            <type>quest item</type>
        </types>
        <rarity>artifact</rarity>
    </item>
    <item>
        <name>dagger</name>
        <cost>2</cost>
        <damage>2</damage>
        <criticalRange>11</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>1</weight>
        <damageTypes>
            <damageType>piercing</damageType>
            <damageType>slashing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_DAGGER_1</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>light weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>light mace</name>
        <cost>5</cost>
        <damage>3</damage>
        <criticalRange>12</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>4</weight>
        <damageTypes>
            <damageType>bludgeoning</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_LIGHT_MACE</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>light weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>sickle</name>
        <cost>6</cost>
        <damage>3</damage>
        <criticalRange>12</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>2</weight>
        <damageTypes>
            <damageType>slashing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_SICKLE</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>light weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>club</name>
        <cost>0</cost>
        <damage>3</damage>
        <criticalRange>12</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>3</weight>
        <damageTypes>
            <damageType>bludgeoning</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_CLUB</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>one-handed weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>heavy mace</name>
        <cost>12</cost>
        <damage>4</damage>
        <criticalRange>12</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>8</weight>
        <damageTypes>
            <damageType>bludgeoning</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_MACE</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>one-handed weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>morning star</name>
        <cost>8</cost>
        <damage>4</damage>
        <criticalRange>12</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>5</weight>
        <damageTypes>
            <damageType>bludgeoning</damageType>
            <damageType>piercing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_MORNING_STAR_1</icon>
            <icon>ITEM_MORNING_STAR_2</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>one-handed weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>short spear</name>
        <cost>1</cost>
        <damage>3</damage>
        <criticalRange>12</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>3</weight>
        <damageTypes>
            <damageType>piercing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_SHORTSPEAR</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>one-handed weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>longspear</name>
        <cost>5</cost>
        <damage>4</damage>
        <criticalRange>12</criticalRange>
        <criticalDamage>3</criticalDamage>
        <weight>9</weight>
        <damageTypes>
            <damageType>piercing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_LONGSPEAR</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>two-handed weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>spear</name>
        <cost>2</cost>
        <damage>4</damage>
        <criticalRange>12</criticalRange>
        <criticalDamage>3</criticalDamage>
        <weight>6</weight>
        <damageTypes>
            <damageType>piercing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_SPEAR</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>two-handed weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>short sword</name>
        <cost>10</cost>
        <damage>3</damage>
        <criticalRange>11</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>2</weight>
        <damageTypes>
            <damageType>piercing</damageType>
        </damageTypes>
        <class>martial</class>
        <icons>
            <icon>ITEM_SHORT_SWORD_1</icon>
            <icon>ITEM_SHORT_SWORD_2</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>light weapon</type>
            <type>melee</type>
            <type>martial weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>healing potion</name>
        <cost>150</cost>
        <weight>1</weight>
        <charges>1</charges>
        <effects>
                <effect type="on drink" name="healing" power="1d10" />
        </effects>
        <icons>
                <icon>ITEM_POTION_1</icon>
        </icons>
        <types>
                <type>potion</type>
        </types>
        <rarity>uncommon</rarity>
    </item>
    <item>
        <name>minor healing potion</name>
        <cost>100</cost>
        <weight>1</weight>
        <charges>1</charges>
        <effects>
                <effect type="on drink" name="healing" power="1d6" />
        </effects>
        <icons>
                <icon>ITEM_POTION_1</icon>
        </icons>
        <types>
                <type>potion</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>minor potion of poison</name>
        <cost>100</cost>
        <weight>1</weight>
        <charges>1</charges>
        <effects>
                <effect type="on drink" name="damage" power="1d6" />
        </effects>
        <icons>
                <icon>ITEM_POTION_1</icon>
        </icons>
        <types>
                <type>potion</type>
        </types>
        <rarity>common</rarity>
    </item>
</items>
"""

        creatureConfig = """
<creatures>
    <creature>
        <name>rat</name>
        <body>4</body>
        <finesse>12</finesse>
        <mind>2</mind>
        <hp>2</hp>
        <speed>2</speed>
        <icons>
            <icon>CREATURE_RAT_1</icon>
            <icon>CREATURE_RAT_2</icon>
            <icon>CREATURE_RAT_3</icon>
            <icon>CREATURE_RAT_4</icon>
        </icons>
        <attack>2</attack>
        <size>small</size>
    </creature>
    <creature>
        <name>fire beetle</name>
        <body>10</body>
        <finesse>11</finesse>
        <mind>0</mind>
        <hp>4</hp>
        <speed>1.9</speed>
        <icons>
            <icon>CREATURE_BEETLE_1</icon>
            <icon>CREATURE_BEETLE_2</icon>
        </icons>
        <attack>4</attack>
        <size>small</size>
    </creature>
    <creature>
        <name>gargoyle</name>
        <body>15</body>
        <finesse>14</finesse>
        <mind>6</mind>
        <hp>37</hp>
        <speed>1</speed>
        <icons>
            <icon>CREATURE_GARGOYLE</icon>
        </icons>
        <attack>4</attack>
        <size>medium</size>
        <feats>
            <feat name="toughness" />
            <feat name="multiattack" />
            <feat name="damage reduction" type="magic" amount="10" />
            <feat name="darkvision" range="10" />
            <feat name="mimic" target="gargoyle statue" />
        </feats>
    </creature>
</creatures>
"""
        walk_factory = WalkFactory()
        move_factory = MoveFactory(walk_factory)

        unarmed_combat_factory = UnarmedCombatFactory()
        melee_combat_factory = MeleeCombatFactory()
        attack_factory = AttackFactory([
                                        unarmed_combat_factory,
                                        melee_combat_factory])

        self.action_factory = ActionFactory(
                                            StubModel(),
                                            [move_factory, attack_factory])

        self.model = pyherc.data.model.Model()
        self.item_generator = pyherc.generators.item.ItemGenerator()
        self.creatureGenerator = pyherc.generators.CreatureGenerator(self.action_factory)
        self.tables = pyherc.rules.tables.Tables()
        self.tables.load_tables(None, itemConfig, creatureConfig)
        self.model.tables = self.tables

        self.setUp2()

    def setUp2(self):
        pass

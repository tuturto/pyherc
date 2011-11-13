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

import pyHerc.data.dungeon
import pyHerc.data.model
import pyHerc.rules.tables

from pyHerc.rules.public import ActionFactory
from pyHerc.rules.move.factories import MoveFactory
from pyHerc.rules.move.factories import WalkFactory

from pyHerc.rules.attack.factories import UnarmedCombatFactory
from pyHerc.rules.attack.factories import AttackFactory

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

    def raise_event(self, event):
        pass

class IntegrationTest():

    def setup(self):
        itemConfig = """
<items>
    <item>
        <name>apple</name>
        <cost>1</cost>
        <weight>1</weight>
        <icons>
            <icon>item_apple</icon>
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
            <icon>item_crystal_skull</icon>
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
            <icon>item_dagger_1</icon>
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
            <icon>item_light_mace</icon>
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
            <icon>item_sickle</icon>
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
            <icon>item_club</icon>
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
            <icon>item_mace</icon>
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
            <icon>item_morning_star_1</icon>
            <icon>item_morning_star_2</icon>
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
            <icon>item_shortspear</icon>
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
            <icon>item_longspear</icon>
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
            <icon>item_spear</icon>
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
            <icon>item_short_sword_1</icon>
            <icon>item_short_sword_2</icon>
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
                <icon>item_potion_1</icon>
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
                <icon>item_potion_1</icon>
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
                <icon>item_potion_1</icon>
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
        <str>4</str>
        <dex>12</dex>
        <con>4</con>
        <int>2</int>
        <wis>4</wis>
        <cha>4</cha>
        <hp>2</hp>
        <speed>2</speed>
        <icons>
            <icon>creature_rat_1</icon>
            <icon>creature_rat_2</icon>
            <icon>creature_rat_3</icon>
            <icon>creature_rat_4</icon>
        </icons>
        <attack>1d4</attack>
        <size>small</size>
    </creature>
    <creature>
        <name>fire beetle</name>
        <str>10</str>
        <dex>11</dex>
        <con>11</con>
        <int>0</int>
        <wis>10</wis>
        <cha>7</cha>
        <hp>4</hp>
        <speed>1.9</speed>
        <icons>
            <icon>creature_beetle_1</icon>
            <icon>creature_beetle_2</icon>
        </icons>
        <attack>2d4</attack>
        <size>small</size>
    </creature>
    <creature>
        <name>gargoyle</name>
        <str>15</str>
        <dex>14</dex>
        <con>18</con>
        <int>6</int>
        <wis>11</wis>
        <cha>7</cha>
        <hp>37</hp>
        <speed>1</speed>
        <icons>
            <icon>CREATURE_GARGOYLE</icon>
        </icons>
        <attack>1d4+2</attack>
        <size>medium</size>
        <feats>
            <feat name="toughness" />
            <feat name="multiattack" />
            <feat name="damage reduction" type="magic" amount="10" />
            <feat name="darkvision" range="10" />
            <feat name="freeze" />
        </feats>
    </creature>
</creatures>
"""

        walk_factory = WalkFactory()
        move_factory = MoveFactory([walk_factory])

        unarmed_combat = UnarmedCombatFactory()
        attack_factory = AttackFactory([unarmed_combat])

        self.action_factory = ActionFactory([move_factory, attack_factory])

        self.model = pyHerc.data.model.Model()
        self.itemGenerator = pyHerc.generators.item.ItemGenerator()
        self.creatureGenerator = pyHerc.generators.creature.CreatureGenerator(self.action_factory)
        self.tables = pyHerc.rules.tables.Tables()
        self.tables.load_tables(itemConfig, creatureConfig)
        self.model.tables = self.tables

        self.setUp2()

    def setUp2(self):
        pass

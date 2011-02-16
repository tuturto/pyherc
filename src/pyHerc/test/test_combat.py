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

from pyHerc.data.dungeon import Level
import pyHerc.generators.item
import pyHerc.rules.combat
import pyHerc.data.model
import pyHerc.rules.tables

class test_meleeCombat:

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
        <damage>1d4</damage>
        <criticalRange>19</criticalRange>
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
        <name>longspear</name>
        <cost>5</cost>
        <damage>1d8</damage>
        <criticalRange>20</criticalRange>
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
        <name>sickle</name>
        <cost>6</cost>
        <damage>1d6</damage>
        <criticalRange>20</criticalRange>
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
        <damage>1d6</damage>
        <criticalRange>20</criticalRange>
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
</items>
"""
        self.model = pyHerc.data.model.Model()
        self.generator = pyHerc.generators.item.ItemGenerator()
        self.tables = pyHerc.rules.tables.Tables()
        self.tables.loadTables(itemConfig)
        self.model.tables = self.tables

    def test_getArmourClass_simple(self):
        """
        Test simple calculation of armour class
        """
        # def getArmourClass(model, character):
        #10 + armor bonus + shield bonus + Dexterity modifier + size modifier
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.dex = 16 # +3 bonus

        ac = pyHerc.rules.combat.getArmourClass(self.model, character)

        assert(ac == 15)

    def test_checkHitInMelee_simple(self):
        # def checkHitInMelee(model, attacker, target, dice = []):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        hit = pyHerc.rules.combat.checkHitInMelee(self.model, character, target, [16])
        assert(hit == 1)

    def test_getDamageInMelee_simple(self):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        character.attack = '1d4+1' #hotshot with special fists

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(self.model, character, target, dice = [5])
        assert(damage.amount == 8)
        assert(damage.magicBonus == 0)

    def test_getDamageInMelee_negativeDamage(self):
        character = pyHerc.data.model.Character()
        character.size = 'tiny'
        character.str = 1 # -5 bonus
        character.attack = '1d3'

        target = pyHerc.data.model.Character()
        target.size = 'medium'
        target.dex = 10

        damage = pyHerc.rules.combat.getDamageInMelee(self.model, character, target, dice = [3])
        assert(damage.amount == 1)
        assert(damage.magicBonus == 0)

    def test_getDamageInMelee_wieldWeaponWithTwoHands(self):
        """
        Test that character wearing a single-handed weapon two-handedly gets the 1.5 * str bonus
        """
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus

        weapon = self.generator.generateItem(self.tables, {'name' : 'club'})

        character.attack = '1d4'
        character.weapons = [weapon]

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(self.model, character, target, dice = [6])
        assert(damage.amount == 11) # 1d6 from weapon + 3 from str + 1.5 from str while wielding 2-handed

    def test_getDamageInMelee_wieldSicleWithTwoHands(self):
        """
        Test that character wearing a light weapon (sickle) two-handedly gets the 1 * str bonus
        Check that damage type is correct
        """
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus

        weapon = self.generator.generateItem(self.tables, {'name' : 'sickle'})

        character.attack = '1d4'
        character.weapons = [weapon]

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(self.model, character, target, dice = [6])
        assert(damage.amount == 9) # 1d6 from weapon + 3 from str
        assert('slashing' in damage.type)

    def test_getDamageInMelee_mundaneItem(self):
        """
        Test that character wearing an apple can use it as a weapon
        Check that damage type is correct
        """
        character = pyHerc.data.model.Character()
        character.size = 'medium'
        character.str = 16

        weapon = self.generator.generateItem(self.tables, {'name' : 'apple'})

        character.attack = '1d4'
        character.weapons = [weapon]

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(self.model, character, target)
        assert(damage.amount == 4) # 1 from apple, +3 strength bonus
        assert('bludgeoning' in damage.type)

    def test_getDamageInMelee_noPrerolls(self):
        """
        Just simple test that damage in melee is possible without prerolled scores
        """
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        character.attack = '1d4'

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(self.model, character, target)

    def test_melee(self):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        character.attack = '1d4'
        character.speed = 1
        character.tick = 0

        level = level = Level((20, 20), 0, 0)
        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus
        target.hp = 10
        level.addCreature(character, (10, 10))
        level.addCreature(target, (11, 10))

        pyHerc.rules.combat.meleeAttack(self.model, character, target, dice = [4, 19])
        assert(target.hp == 3) # 10 - 4 - 3 (hp - damage roll - str bonus)

    def test_dyingInMelee(self):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        character.attack = '1d4'
        character.speed = 1
        character.tick = 0

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus
        target.hp = 5

        level = Level((20, 20), 0, 0)
        level.addCreature(character)
        level.addCreature(target)

        pyHerc.rules.combat.meleeAttack(self.model, character, target, dice = [4, 19])
        assert(target.hp == -2) # 5 - 4 - 3 (hp - damage roll - str bonus)
        assert(not target in level.creatures)

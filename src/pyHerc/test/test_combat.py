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

# def getDamageInMelee(model, attacker, target, dice = []):

from pyHerc.data.dungeon import Level
import pyHerc.generators.item
import pyHerc.rules.combat
import pyHerc.data.model
import pyHerc.rules.tables

class test_meleeCombat:

    def test_getArmourClass_simple(self):
        """
        Test simple calculation of armour class
        """
        # def getArmourClass(model, character):
        #10 + armor bonus + shield bonus + Dexterity modifier + size modifier
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.dex = 16 # +3 bonus
        model = pyHerc.data.model.Model()
        tables = pyHerc.rules.tables.Tables()
        tables.loadTables()
        model.tables = tables
        ac = pyHerc.rules.combat.getArmourClass(model, character)

        assert(ac == 15)


    def test_checkHitInMelee_simple(self):
        # def checkHitInMelee(model, attacker, target, dice = []):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        model = pyHerc.data.model.Model()
        tables = pyHerc.rules.tables.Tables()
        tables.loadTables()
        model.tables = tables
        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        hit = pyHerc.rules.combat.checkHitInMelee(model, character, target, [16])
        assert(hit == 1)

    def test_getDamageInMelee_simple(self):
        #def getDamageInMelee(model, attacker, target, dice = []):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        character.attack = '1d4+1' #hotshot with special fists

        model = pyHerc.data.model.Model()
        tables = pyHerc.rules.tables.Tables()
        tables.loadTables()
        model.tables = tables
        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(model, character, target, dice = [5])
        assert(damage.amount == 8)
        assert(damage.magicBonus == 0)

    def test_getDamageInMelee_wieldWeaponWithTwoHands(self):
        """
        Test that character wearing a single-handed weapon two-handedly gets the 1.5 * str bonus
        """
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus

        model = pyHerc.data.model.Model()
        tables = pyHerc.rules.tables.Tables()
        tables.loadTables()
        model.tables = tables

        generator = pyHerc.generators.item.ItemGenerator()
        weapon = generator.generateItem(tables, {'name' : 'club'})

        character.attack = '1d4'
        character.weapons = [weapon]

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(model, character, target, dice = [6])
        assert(damage.amount == 11) # 1d6 from weapon + 3 from str + 1.5 from str while wielding 2-handed

    def test_getDamageInMelee_wieldSicleWithTwoHands(self):
        """
        Test that character wearing a light weapon (sickle) two-handedly gets the 1 * str bonus
        Check that damage type is correct
        """
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus

        model = pyHerc.data.model.Model()
        tables = pyHerc.rules.tables.Tables()
        tables.loadTables()
        model.tables = tables

        generator = pyHerc.generators.item.ItemGenerator()
        weapon = generator.generateItem(tables, {'name' : 'sickle'})

        character.attack = '1d4'
        character.weapons = [weapon]

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(model, character, target, dice = [6])
        assert(damage.amount == 9) # 1d6 from weapon + 3 from str
        assert('slashing' in damage.type)

    def test_getDamageInMelee_noPrerolls(self):
        """
        Just simple test that damage in melee is possible without prerolled scores
        """
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        character.attack = '1d4'

        model = pyHerc.data.model.Model()
        tables = pyHerc.rules.tables.Tables()
        tables.loadTables()
        model.tables = tables
        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(model, character, target)

    def test_melee(self):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        character.attack = '1d4'
        character.speed = 1
        character.tick = 0

        model = pyHerc.data.model.Model()
        tables = pyHerc.rules.tables.Tables()
        tables.loadTables()
        model.tables = tables
        level = level = Level((20, 20), 0, 0)
        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus
        target.hp = 10
        level.addCreature(character, (10, 10))
        level.addCreature(target, (11, 10))

        pyHerc.rules.combat.meleeAttack(model, character, target, dice = [4, 19])
        assert(target.hp == 3) # 10 - 4 - 3 (hp - damage roll - str bonus)

    def test_dyingInMelee(self):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        character.attack = '1d4'
        character.speed = 1
        character.tick = 0

        model = pyHerc.data.model.Model()
        tables = pyHerc.rules.tables.Tables()
        tables.loadTables()
        model.tables = tables
        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus
        target.hp = 5

        level = Level((20, 20), 0, 0)
        level.addCreature(character)
        level.addCreature(target)

        pyHerc.rules.combat.meleeAttack(model, character, target, dice = [4, 19])
        assert(target.hp == -2) # 5 - 4 - 3 (hp - damage roll - str bonus)
        assert(not target in level.creatures)

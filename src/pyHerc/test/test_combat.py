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
from pyHerc.test import IntegrationTest
import pyHerc.generators.item
import pyHerc.rules.combat
import pyHerc.data.model
import pyHerc.rules.tables

class test_meleeCombat(IntegrationTest):

    def test_get_armour_class_simple(self):
        """
        Test simple calculation of armour class
        """
        # def get_armour_class(model, character):
        #10 + armor bonus + shield bonus + Dexterity modifier + size modifier
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.dex = 16 # +3 bonus

        ac = pyHerc.rules.combat.get_armour_class(self.model, character)

        assert(ac == 15)

    def test_check_hit_in_melee_simple(self):
        # def check_hit_in_melee(model, attacker, target, dice = []):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        hit = pyHerc.rules.combat.check_hit_in_melee(self.model, character, target, [16])
        assert(hit == 1)

    def test_get_damage_in_melee_simple(self):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        character.attack = '1d4+1' #hotshot with special fists

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.get_damage_in_melee(self.model, character, target, dice = [5])
        assert(damage.amount == 8)
        assert(damage.magicBonus == 0)

    def test_get_damage_in_melee_negative_damage(self):
        character = pyHerc.data.model.Character()
        character.size = 'tiny'
        character.str = 1 # -5 bonus
        character.attack = '1d3'

        target = pyHerc.data.model.Character()
        target.size = 'medium'
        target.dex = 10

        damage = pyHerc.rules.combat.get_damage_in_melee(self.model, character, target, dice = [3])
        assert(damage.amount == 1)
        assert(damage.magicBonus == 0)

    def test_get_damage_in_melee_wield_weapon_with_two_hands(self):
        """
        Test that character wearing a single-handed weapon two-handedly gets the 1.5 * str bonus
        """
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus

        weapon = self.itemGenerator.generateItem(self.tables, {'name' : 'club'})

        character.attack = '1d4'
        character.weapons = [weapon]

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.get_damage_in_melee(self.model, character, target, dice = [6])
        assert(damage.amount == 11) # 1d6 from weapon + 3 from str + 1.5 from str while wielding 2-handed

    def test_get_damage_in_melee_wield_sicle_with_two_hands(self):
        """
        Test that character wearing a light weapon (sickle) two-handedly gets the 1 * str bonus
        Check that damage type is correct
        """
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus

        weapon = self.itemGenerator.generateItem(self.tables, {'name' : 'sickle'})

        character.attack = '1d4'
        character.weapons = [weapon]

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.get_damage_in_melee(self.model, character, target, dice = [6])
        assert(damage.amount == 9) # 1d6 from weapon + 3 from str
        assert('slashing' in damage.type)

    def test_get_damage_in_melee_mundane_item(self):
        """
        Test that character wearing an apple can use it as a weapon
        Check that damage type is correct
        """
        character = pyHerc.data.model.Character()
        character.size = 'medium'
        character.str = 16

        weapon = self.itemGenerator.generateItem(self.tables, {'name' : 'apple'})

        character.attack = '1d4'
        character.weapons = [weapon]

        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.get_damage_in_melee(self.model, character, target)
        assert(damage.amount == 4) # 1 from apple, +3 strength bonus
        assert('bludgeoning' in damage.type)

    def test_get_damage_in_melee_no_prerolls(self):
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

        damage = pyHerc.rules.combat.get_damage_in_melee(self.model, character, target)

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

        pyHerc.rules.combat.melee_attack(self.model, character, target, dice = [4, 19])
        assert(target.hp == 3) # 10 - 4 - 3 (hp - damage roll - str bonus)

    def test_dying_in_melee(self):
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

        pyHerc.rules.combat.melee_attack(self.model, character, target, dice = [4, 19])
        assert(target.hp == -2) # 5 - 4 - 3 (hp - damage roll - str bonus)
        assert(not target in level.creatures)

    def test_simple_weapon_proficiency_modifier(self):
        '''
        Simple test that weapon proficiency modifier can be calculated
        '''
        character = pyHerc.data.model.Character()
        weapon = self.itemGenerator.generateItem(self.tables, {'name' : 'club'})

        character.attack = '1d4'
        character.weapons = [weapon]
        character.feats = []

        modifier = pyHerc.rules.combat.get_weapon_proficiency_modifier(self.model, character, weapon)
        assert(modifier == -4)

        character.feats.append(
                               pyHerc.data.model.WeaponProficiency(
                               'simple'))

        modifier = pyHerc.rules.combat.get_weapon_proficiency_modifier(self.model, character, weapon)
        assert(modifier == 0)

    def test_martial_weapon_proficiency_modifier(self):
        '''
        Simple test that weapon proficiency modifier can be calculated for martial weapons
        '''
        character = pyHerc.data.model.Character()
        weapon = self.itemGenerator.generateItem(self.tables, {'name' : 'short sword'})

        character.attack = '1d4'
        character.weapons = [weapon]
        character.feats = []

        modifier = pyHerc.rules.combat.get_weapon_proficiency_modifier(self.model, character, weapon)
        assert(modifier == -4)

        character.feats.append(
                               pyHerc.data.model.WeaponProficiency(
                               'martial'))

        modifier = pyHerc.rules.combat.get_weapon_proficiency_modifier(self.model, character, weapon)
        assert(modifier == 0)

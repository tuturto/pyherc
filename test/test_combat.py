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

import pyHerc.rules.combat
import pyHerc.data.model

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

        ac = pyHerc.rules.combat.getArmourClass(model, character)

        assert(ac == 15)


    def test_checkHitInMelee_simple(self):
        # def checkHitInMelee(model, attacker, target, dice = []):
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        model = pyHerc.data.model.Model()
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

        model = pyHerc.data.model.Model()
        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(model, character, target, dice = [5])
        assert(damage == 8)

    def test_getDamageInMelee_noPrerolls(self):
        """
        Just simple test that damage in melee is possible without prerolled scores
        """
        character = pyHerc.data.model.Character()
        character.size = 'tiny' # +2 bonus
        character.str = 16 # +3 bonus
        character.attack = '1d4'

        model = pyHerc.data.model.Model()
        target = pyHerc.data.model.Character()
        target.size = 'medium' # +0 bonus
        target.dex = 10 # no bonus

        damage = pyHerc.rules.combat.getDamageInMelee(model, character, target)

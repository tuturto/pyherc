#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2011 Tuukka Turto
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

'''
Module defining classes related to AttackAction
'''
import pyHerc.rules.time
import pyHerc.rules.ending

class AttackAction():
    '''
    Action for attacking
    '''
    def __init__(self, attack_type, to_hit, damage, attacker, target, model):
        '''
        Default constructor
        @attack_type: type of the attack
        @param to_hit: ToHit object for calculating if attack hits
        @param damage: Damage object for calculating done damage
        @param attacker: Character doing attack
        @param target: Character being attacked
        '''
        self.action_type = 'attack'
        self.attack_type = attack_type
        self.to_hit = to_hit
        self.damage = damage
        self.attacker = attacker
        self.target = target
        self.model = model

    def execute(self):
        '''
        Executes this Attack
        '''
        if self.to_hit.is_hit():
            self.damage.apply_damage(self.target)
            #TODO: raise events

        pyHerc.rules.ending.check_dying(self.model, self.target, self.model)

        #TODO: just a temporary time
        self.attacker.tick = pyHerc.rules.time.get_new_tick(self.attacker, 20)


class ToHit():
    '''
    Checks done for hitting
    '''

    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def is_hit(self):
        '''
        Checks if the hit lands
        @returns: True if hit is successful, False otherwise
        '''
        pass

class Damage():
    '''
    Damage done in attack
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def apply_damage(self, target):
        '''
        Applies damage to target
        @param target: Target to damage
        '''
        target.set_hp(target.get_hp() - self.damage)

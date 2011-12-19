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
Module defining unarmed attack related objcts

Classes:
UnarmedToHit
UnarmedDamage
'''
import logging
import random

from pyHerc.rules.attack.action import ToHit
from pyHerc.rules.attack.action import Damage

class UnarmedToHit(ToHit):

    def __init__(self, attacker,  target,
                        random_number_generator = random.Random()):
        '''
        Default constructor

        @param attacker: Character doing the attack
        @param target: Character being attacked
        @param rng: Random number generator
        '''
        self.logger = logging.getLogger('pyHerc.rules.attack.unarmed.UnarmedToHit')
        self.attacker = attacker
        self.target = target
        self.rng = random_number_generator

    def is_hit(self):
        '''
        Checks if the hit lands
        @returns: True if hit is successful, False otherwise
        '''
        self.logger.debug('Checking for hit')

        target_number = self.attacker.get_body()
        self.logger.debug('Target number is {0}'.format(target_number))

        to_hit_roll = self.rng.randint(1, 6) + self.rng.randint(1, 6)
        self.logger.debug('Rolled {0} for to hit'.format(to_hit_roll))

        if (to_hit_roll <= target_number) or (to_hit_roll == 2):
            is_hit = True
        else:
            is_hit = False

        self.logger.debug('Hit: {0}'.format(is_hit))
        return is_hit

class UnarmedDamage(Damage):
    '''
    Damage done in unarmed attack
    '''
    def __init__(self, damage):
        '''
        Default constructor
        '''
        self.logger = logging.getLogger('pyHerc.rules.attack.unarmed.UnarmedDamage')
        self.damage = damage

    def apply_damage(self, target):
        '''
        Applies damage to target
        @param target: Target to damage
        '''
        self.logger.debug('Applying damage of {0}'.format(self.damage))
        target.set_hp(target.get_hp() - self.damage)

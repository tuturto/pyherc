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
from pyHerc.rules.public import Action

class AttackAction(Action):
    '''
    Action for attacking
    '''
    def __init__(self, attack_type, to_hit, damage):
        '''
        Default constructor
        @attack_type: type of the attack
        @param to_hit: ToHit object for calculating if attack hits
        @param damage: Damage object for calculating done damage
        '''
        self.action_type = 'attack'
        self.attack_type = attack_type
        self.to_hit = to_hit
        self.damage = damage


    def execute(self):
        '''
        Executes this Attack
        '''
        pass

class ToHit():
    '''
    Checks done for hitting
    '''
    pass

class Damage():
    '''
    Damage done in attack
    '''
    pass

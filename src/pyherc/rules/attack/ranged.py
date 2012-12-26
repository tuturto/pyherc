#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module for ranged combat
"""
from pyherc.aspects import logged
from pyherc.rules.attack.action import ToHit
from pyherc.rules.attack.action import Damage

class RangedToHit(ToHit):
    """
    Class to perform to hit calculations in ranged combat

    .. versionadded:: 0.8
    """

    @logged
    def __init__(self, attacker, target, rng):
        """
        Default constructor

        :param attacker: character attacking
        :type attacker: Character
        :param target: target of the attack
        :type target: Character
        :rng: random number generator
        """
        self.attacker = attacker
        self.target = target
        self.rng = rng

class RangedDamage(Damage):
    """
    Damage done with ranged attack

    .. versionadded:: 0.8
    """

    @logged
    def __init__(self, damage):
        """
        Default constructor
        """
        super(RangedDamage, self).__init__(damage)

class RangedCombatFactory(object):
    """
    Factory for producing ranged combat actions

    .. versionadded:: 0.8
    """
    @logged
    def __init__(self, effect_factory, dying_rules):
        """
        Constructor for this factory
        """
        self.attack_type = 'ranged'
        self.effect_factory = effect_factory
        self.dying_rules = dying_rules

    @logged
    def can_handle(self, parameters):
        """
        Can this factory process these parameters

        :param parameters: parameters to check
        :type parameters: AttackParameters
        :returns: true if factory is capable of handling parameters
        :rtype: boolean
        """
        return self.attack_type == parameters.attack_type

    @logged
    def get_action(self, parameters):
        """
        Create a attack action

        :param parameters: parameters used to control attack creation
        :type parameters: AttackParameters
        :returns: action that can be executed
        :rtype: AttackAction
        """
        attacker = parameters.attacker
        target = self.get_target(parameters)
        weapon = attacker.inventory.weapon
        weapon_data = weapon.weapon_data

        attack = AttackAction(
                    attack_type = 'ranged',
                    to_hit = RangedToHit(attacker, target,
                                         parameters.random_number_generator),
                    damage = RangedDamage(damage = weapon_data.damage),
                    attacker = attacker,
                    target = target,
                    effect_factory = self.effect_factory,
                    dying_rules = self.dying_rules)

        return attack

    @logged
    def get_target(self, parameters):
        """
        Get target of the attack

        :param parameters: parameters to control attack
        :type parameters: MeleeAttackParameters
        :returns: target character if found, otherwise None
        :rtype: Character
        """
        return None

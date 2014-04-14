# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
from pyherc.aspects import log_debug, log_info
from pyherc.data.damage import Damage
from pyherc.data.geometry import get_target_in_direction
from pyherc.rules.combat.action import AttackAction, ToHit


class RangedToHit(ToHit):
    """
    Class to perform to hit calculations in ranged combat

    .. versionadded:: 0.8
    """

    @log_debug
    def __init__(self, attacker, target, rng):
        """
        Default constructor

        :param attacker: character attacking
        :type attacker: Character
        :param target: target of the attack
        :type target: Character
        :rng: random number generator
        """
        super().__init__(attacker, target, rng)


class RangedCombatFactory():
    """
    Factory for producing ranged combat actions

    .. versionadded:: 0.8
    """
    @log_debug
    def __init__(self, effect_factory, dying_rules):
        """
        Constructor for this factory
        """
        super().__init__()
        self.attack_type = 'ranged'
        self.effect_factory = effect_factory
        self.dying_rules = dying_rules

    @log_debug
    def can_handle(self, parameters):
        """
        Can this factory process these parameters

        :param parameters: parameters to check
        :type parameters: AttackParameters
        :returns: true if factory is capable of handling parameters
        :rtype: boolean
        """
        return self.attack_type == parameters.attack_type

    @log_info
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
        weapon = attacker.inventory.projectiles
        ammo_data = weapon.ammunition_data

        attack = AttackAction(
            attack_type='ranged',
            to_hit=RangedToHit(attacker,
                               target,
                               parameters.random_number_generator),
            damage=Damage(damage=ammo_data.damage),
            attacker=attacker,
            target=target,
            effect_factory=self.effect_factory,
            dying_rules=self.dying_rules,
            additional_rules=AdditionalRangedRules(attacker))

        return attack

    @log_debug
    def get_target(self, parameters):
        """
        Get target of the attack

        :param parameters: parameters to control attack
        :type parameters: MeleeAttackParameters
        :returns: target character if found, otherwise None
        :rtype: Character
        """
        location = parameters.attacker.location
        level = parameters.attacker.level
        direction = parameters.direction

        return get_target_in_direction(level,
                                       location,
                                       direction)


class AdditionalRangedRules():
    """
    Additional rules for ranged attack

    .. versionadded:: 0.8
    """
    @log_debug
    def __init__(self, attacker):
        """
        Default constructor
        """
        super().__init__()

        self.attacker = attacker

    @log_debug
    def after_attack(self):
        """
        Processing happening after an attack
        """
        ammunition = self.attacker.inventory.projectiles
        ammunition.ammunition_data.count = ammunition.ammunition_data.count - 1

        if ammunition.ammunition_data.count <= 0:
            self.attacker.inventory.projectiles = None
            self.attacker.inventory.remove(ammunition)

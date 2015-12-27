# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for ranged combat
"""
from pyherc.aspects import log_debug, log_info
from pyherc.data.damage import new_damage
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
                               parameters.rng),
            damage=new_damage(ammo_data.damage),
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

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
Module defining classes related to AttackAction
"""
import random

from pyherc.aspects import log_debug, log_info
from pyherc.data.constants import Duration
from pyherc.data.damage import new_damage
from pyherc.events import (new_attack_hit_event, new_attack_miss_event,
                           new_attack_nothing_event)


class AttackAction():
    """
    Action for attacking
    """
    @log_debug
    def __init__(self, attack_type, to_hit, damage,
                 attacker, target, effect_factory, dying_rules,
                 additional_rules):
        """
        Default constructor

        :param attack_type: type of the attack
        :type attack_type: string
        :param to_hit: ToHit object for calculating if attack hits
        :type to_hit: ToHit
        :param damage: Damage object for calculating done damage
        :type damage: Damage
        :param attacker: Character doing attack
        :type attacker: Character
        :param target: Character being attacked
        :type target: TargetData
        :param effect_factory: Factory used for creating magic effects
        :type effect_factory: EffectFactory
        :param dying_rules: rules for dying
        :param additional_rules: additional rules
        :type additional_rules: AdditionalRules
        """
        super().__init__()
        self.action_type = 'attack'
        self.attack_type = attack_type
        self.to_hit = to_hit
        self.damage = damage
        self.attacker = attacker
        self.target = target
        self.effect_factory = effect_factory
        self.dying_rules = dying_rules
        self.additional_rules = additional_rules

    @log_debug
    def is_legal(self):
        """
        Check if the attack is possible to perform

        :returns: true if attackis possible, false otherwise
        :rtype: Boolean
        """
        if self.attacker is None:
            return False

        return True

    @log_info
    def execute(self):
        """
        Executes this Attack
        """
        target = self.target.target

        if target is None:
            self.attacker.raise_event(
                new_attack_nothing_event(attacker=self.attacker))
        else:

            was_hit = self.to_hit.is_hit()

            if was_hit:
                damage_caused = self.damage(target)

                self.attacker.raise_event(new_attack_hit_event(
                    type=self.attack_type,
                    attacker=self.attacker,
                    target=target,
                    damage=damage_caused))

                self.__trigger_attack_effects()
            else:
                self.attacker.raise_event(new_attack_miss_event(
                    type=self.attack_type,
                    attacker=self.attacker,
                    target=target))

            self.dying_rules.check_dying(target)

        self.additional_rules.after_attack()
        self.attacker.add_to_tick(self.__get_duration())

    @log_debug
    def __get_duration(self):
        """
        Get duration of the attack

        .. versionadded:: 0.10
        """
        weapon = self.attacker.inventory.weapon

        if weapon:
            return Duration.normal / weapon.weapon_data.speed
        else:
            return Duration.normal

    @log_debug
    def __trigger_attack_effects(self):
        """
        Trigger effects

        .. versionadded:: 0.4
        """
        target = self.target.target

        weapon = self.attacker.inventory.weapon
        effects = self.attacker.get_effect_handles('on attack hit')

        if weapon is not None:
            effects.extend(weapon.get_effect_handles('on attack hit'))
        for effect_spec in effects:
            effect = self.effect_factory(effect_spec.effect, target=target)

            if not effect.duration or effect.duration <= 0:
                effect.trigger(self.dying_rules)
            else:
                target.add_effect(effect)


class ToHit():
    """
    Checks done for hitting
    """
    @log_debug
    def __init__(self, attacker, target,
                 random_number_generator=random.Random()):
        """
        Default constructor
        """
        super().__init__()
        self.attacker = attacker
        self.target = target
        self.rng = random_number_generator

    @log_debug
    def is_hit(self):
        """
        Checks if the hit lands
        @returns: True if hit is successful, False otherwise
        """
        return True


class AdditionalRules():
    """
    Additional rules for attacks

    .. versionadded: 0.8
    """
    @log_debug
    def __init__(self, attacker):
        """
        Default constructor
        """
        super().__init__()

    @log_debug
    def after_attack(self):
        """
        Processing happening after an attack
        """
        pass

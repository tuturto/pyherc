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
Module defining classes related to AttackAction
"""
import random

from pyherc.aspects import log_debug, log_info
from pyherc.data.constants import Duration
from pyherc.data.damage import Damage
from pyherc.events import AttackHitEvent, AttackMissEvent, AttackNothingEvent


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
                AttackNothingEvent(attacker=self.attacker,
                                   affected_tiles=[]))
        else:

            was_hit = self.to_hit.is_hit()

            if was_hit:
                self.damage.apply_damage(target)

                self.attacker.raise_event(AttackHitEvent(
                    type=self.attack_type,
                    attacker=self.attacker,
                    target=target,
                    damage=self.damage,
                    affected_tiles=[target.location]))

                self.__trigger_attack_effects()
            else:
                self.attacker.raise_event(AttackMissEvent(
                    type=self.attack_type,
                    attacker=self.attacker,
                    target=target,
                    affected_tiles=[target.location]))

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

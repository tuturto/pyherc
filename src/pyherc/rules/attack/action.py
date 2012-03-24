#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2011 Tuukka Turto
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
import pyherc.rules.time
import pyherc.rules.ending
import random
import logging
from pyherc.aspects import Logged

class AttackAction():
    """
    Action for attacking
    """
    logged = Logged()

    @logged
    def __init__(self, attack_type, to_hit, damage, attacker, target):
        """
        Default constructor

        Args:
            attack_type: type of the attack
            to_hit: ToHit object for calculating if attack hits
            damage: Damage object for calculating done damage
            attacker: Character doing attack
            target: Character being attacked
        """
        self.action_type = 'attack'
        self.attack_type = attack_type
        self.to_hit = to_hit
        self.damage = damage
        self.attacker = attacker
        self.target = target

    @logged
    def execute(self):
        """
        Executes this Attack
        """
        event = {}
        event['type'] = 'melee'
        event['attacker'] = self.attacker
        event['target'] = self.target
        event['damage'] = self.damage
        event['level'] = self.attacker.level
        event['location'] = self.attacker.location

        if self.to_hit.is_hit():
            self.damage.apply_damage(self.target)
            event['hit'] = True
        else:
            event['hit'] = False

        self.attacker.raise_event(event)

        pyherc.rules.ending.check_dying(self.target.model,
                                        self.target,
                                        self.target.model)

        self.attacker.tick = pyherc.rules.time.get_new_tick(self.attacker, 20)


class ToHit(object):
    """
    Checks done for hitting
    """
    logged = Logged()

    @logged
    def __init__(self, attacker,  target,
                        random_number_generator = random.Random()):
        """
        Default constructor
        """
        self.attacker = attacker
        self.target = target
        self.rng = random_number_generator
        self.logger = logging.getLogger('pyherc.rules.attack.action.ToHit')

    @logged
    def is_hit(self):
        """
        Checks if the hit lands
        @returns: True if hit is successful, False otherwise
        """
        target_number = self.attacker.body

        to_hit_roll = self.rng.randint(1, 6) + self.rng.randint(1, 6)

        if (to_hit_roll <= target_number) or (to_hit_roll == 2):
            is_hit = True
        else:
            is_hit = False

        return is_hit

class Damage(object):
    """
    Damage done in attack
    """
    logged = Logged()

    @logged
    def __init__(self, damage):
        """
        Default constructor
        """
        self.logger = logging.getLogger('pyherc.rules.attack.action.Damage')
        self.damage = damage

    @logged
    def apply_damage(self, target):
        """
        Applies damage to target
        @param target: Target to damage
        """
        target.hit_points = target.hit_points - self.damage

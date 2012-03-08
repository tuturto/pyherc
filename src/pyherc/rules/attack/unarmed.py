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
Module defining unarmed attack related objcts

Classes:
UnarmedToHit
UnarmedDamage
"""
import logging
import random

from pyherc.aspects import Logged
from pyherc.rules.attack.action import ToHit
from pyherc.rules.attack.action import Damage

class UnarmedToHit(ToHit):
    """
    Class to perform to hit calculations in unarmed combat
    """

    @Logged()
    def __init__(self, attacker,  target,
                        random_number_generator = random.Random()):
        """
        Default constructor

        Args:
            attacker: Character doing the attack
            target: Character being attacked
            rng: Random number generator
        """
        self.logger = logging.getLogger('pyherc.rules.attack.unarmed.UnarmedToHit')
        self.attacker = attacker
        self.target = target
        self.rng = random_number_generator

class UnarmedDamage(Damage):
    """
    Damage done in unarmed attack
    """
    logged = Logged()

    @logged
    def __init__(self, damage):
        """
        Default constructor
        """
        self.logger = logging.getLogger('pyherc.rules.attack.unarmed.UnarmedDamage')
        self.damage = damage

    @logged
    def apply_damage(self, target):
        """
        Applies damage to target

        Args:
            target: Target to damage
        """
        target.set_hp(target.get_hp() - self.damage)

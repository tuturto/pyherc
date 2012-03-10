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
Attack related factories are defined here
"""

import types
import logging
from pyherc.aspects import Logged
from pyherc.rules.attack.action import AttackAction
from pyherc.rules.attack.unarmed import UnarmedToHit
from pyherc.rules.attack.unarmed import UnarmedDamage
from pyherc.rules.attack.melee import MeleeToHit
from pyherc.rules.attack.melee import MeleeDamage
from pyherc.rules.factory import SubActionFactory

class AttackFactory(SubActionFactory):
    """
    Factory for constructing attack actions
    """

    @Logged()
    def __init__(self, factories):
        """
        Constructor for this factory
        """
        self.action_type = 'attack'

        if isinstance(factories, types.ListType):
            self.factories = factories
        else:
            self.factories = []
            self.factories.append(factories)


class UnarmedCombatFactory():
    """
    Factory for producing unarmed combat actions
    """
    logged = Logged()

    @logged
    def __init__(self):
        """
        Constructor for this factory
        """
        self.attack_type = 'unarmed'

    def __str__(self):
        return 'unarmed combat factory'

    @logged
    def can_handle(self, parameters):
        """
        Can this factory process these parameters

        Args:
            parameters: Parameters to check

        Returns:
            True if factory is capable of handling parameters
        """
        return self.attack_type == parameters.attack_type

    @logged
    def get_action(self, parameters):
        """
        Create a attack action

        Args:
            parameters: Parameters used to control attack creation

        Returns:
            Action that can be executed
        """
        attacker = parameters.attacker
        target = self.get_target(parameters)

        if target != None:
            attack = AttackAction('unarmed',
                        UnarmedToHit(attacker, target,
                                    parameters.random_number_generator),
                        UnarmedDamage(attacker.get_attack()),
                        attacker,
                        target,
                        parameters.model)
        else:
            attack = None

        return attack

    @logged
    def get_target(self, parameters):
        """
        Get target of the attack

        Args:
            parameters: UnarmedAttackParameters

        Returns:
            target character if found, otherwise None
        """
        attacker = parameters.attacker
        location = attacker.location
        direction = parameters.direction
        level = attacker.level

        if direction == 1:
            target_location = (location[0], location[1] - 1)
        elif direction == 2:
            target_location = (location[0] + 1, location[1] - 1)
        elif direction == 3:
            target_location = (location[0] + 1, location[1])
        elif direction == 4:
            target_location = (location[0] + 1, location[1] + 1)
        elif direction == 5:
            target_location = (location[0], location[1] + 1)
        elif direction == 6:
            target_location = (location[0] - 1, location[1] + 1)
        elif direction == 7:
            target_location = (location[0] - 1, location[1])
        elif direction == 8:
            target_location = (location[0] - 1, location[1] - 1)

        target = level.get_creature_at(target_location)

        return target

class MeleeCombatFactory():
    """
    Factory for producing melee combat actions
    """
    logged = Logged()

    @logged
    def __init__(self):
        """
        Constructor for this factory
        """
        self.attack_type = 'melee'

    def __str__(self):
        return 'melee combat factory'

    @logged
    def can_handle(self, parameters):
        """
        Can this factory process these parameters

        Args:
            parameters: Parameters to check

        Returns:
            True if factory is capable of handling parameters
        """
        return self.attack_type == parameters.attack_type

    @logged
    def get_action(self, parameters):
        """
        Create a attack action

        Args:
            parameters: Parameters used to control attack creation
        """
        attacker = parameters.attacker
        target = self.get_target(parameters)
        weapon = attacker.weapons[0]

        if target != None:
            attack = AttackAction('melee',
                        MeleeToHit(attacker, target,
                                    parameters.random_number_generator),
                        MeleeDamage(weapon.weapon_data.damage),
                        attacker,
                        target,
                        parameters.model)
        else:
            attack = None

        return attack

    @logged
    def get_target(self, parameters):
        """
        Get target of the attack

        Args:
            parameters: UnarmedAttackParameters

        Returns:
            target character if found, otherwise None
        """
        attacker = parameters.attacker
        location = attacker.location
        direction = parameters.direction
        level = attacker.level

        if direction == 1:
            target_location = (location[0], location[1] - 1)
        elif direction == 2:
            target_location = (location[0] + 1, location[1] - 1)
        elif direction == 3:
            target_location = (location[0] + 1, location[1])
        elif direction == 4:
            target_location = (location[0] + 1, location[1] + 1)
        elif direction == 5:
            target_location = (location[0], location[1] + 1)
        elif direction == 6:
            target_location = (location[0] - 1, location[1] + 1)
        elif direction == 7:
            target_location = (location[0] - 1, location[1])
        elif direction == 8:
            target_location = (location[0] - 1, location[1] - 1)

        target = level.get_creature_at(target_location)

        return target

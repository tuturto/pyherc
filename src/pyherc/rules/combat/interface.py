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
Public interface for combat rules
"""

from pyherc.aspects import log_debug, log_info
from pyherc.rules.public import ActionParameters
from pyherc.data import blocks_movement, get_character


@log_info
def attack(character, direction, action_factory, rng):
    """
    Attack to given direction

    :param direction: direction to attack
    :type direction: integer
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory
    :param rng: random number generator
    :type rng: Random
    """
    if character.inventory.weapon is not None:
        weapon = character.inventory.weapon.weapon_data
        if character.inventory.projectiles is not None:
            ammunition = character.inventory.projectiles.ammunition_data
        else:
            ammunition = None
    else:
        weapon = None

    if weapon is None:
        attack_type = 'unarmed'
    else:
        if (ammunition is None or
                weapon.ammunition_type != ammunition.ammunition_type):
            attack_type = 'melee'
        else:
            target_loc = character.get_location_at_direction(direction)
            if get_character(character.level, target_loc) is None:
                if blocks_movement(character.level, target_loc):
                    attack_type = 'melee'
                else:
                    attack_type = 'ranged'
            else:
                attack_type = 'melee'

    action = action_factory.get_action(
        AttackParameters(attacker=character,
                         direction=direction,
                         attack_type=attack_type,
                         random_number_generator=rng))

    action.execute()


class AttackParameters(ActionParameters):
    """
    Object for controlling attack action creation
    """

    @log_debug
    def __init__(self, attacker, direction, attack_type,
                 random_number_generator):
        """
        Construct AttackParameters

        Args:
            attacker: Character doing an attack
            direction: Direction to attack to
            attack_type: type of attack to perform
            random_number_generator: Random number generator to use
        """
        super().__init__()

        self.action_type = 'attack'
        self.attacker = attacker
        self.direction = direction
        self.attack_type = attack_type
        self.random_number_generator = random_number_generator
        self.model = None

    @log_debug
    def __str__(self):
        """
        Get string representation of this object
        """
        return 'attack with attack type of ' + self.attack_type

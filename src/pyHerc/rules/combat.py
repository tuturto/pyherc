#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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

import logging
from pyHerc.rules import tables
from pyHerc.rules import utils
from pyHerc.rules import time
from pyHerc.rules import ending
from pyHerc.data.model import Damage
import random

__logger = logging.getLogger('pyHerc.rules.combat')

def melee_attack(model, attacker, target, dice = []):
    """
    Perform single round of attacking in melee
    @param model: model of the world
    @param attacker: character attacking
    @param target: target of the attack
    @param dice: prerolled dice
    """
    assert(model != None)
    assert(attacker != None)
    assert(target != None)
    assert(dice != None)

    event = {}
    event['type'] = 'melee'
    event['attacker'] = attacker
    event['target'] = target
    event['location'] = attacker.location
    event['level'] = attacker.level

    __logger.debug(attacker.__str__() + ' is attacking ' + target.__str__())
    hit = check_hit_in_melee(model, attacker, target, dice)

    event['hit'] = hit

    if hit:
        __logger.debug('attack hits')
        damage = get_damage_in_melee(model, attacker, target, dice)

        if damage.amount < 1:
            damage.amount = 1
        __logger.debug('attack does ' + damage.amount.__str__() + ' points of damage')
        event['damage'] = damage
        #TODO: resistances
        target.hp = target.hp - damage.amount
        __logger.debug(target.__str__() + ' has ' + target.hp.__str__() + ' hp left')
        model.raise_event(event)
        if target.hp < 0:
            ending.checkDying(model, target, None)
    else:
        __logger.debug('attack misses')
        model.raise_event(event)

    attacker.tick = time.getNewTick(attacker, 6)

def check_hit_in_melee(model, attacker, target, dice = []):
    """
    Checks if attacker hits target
    @param attacker: character attacking
    @param target: target of the attack
    @param dice: optional prerolled dice
    """
    assert(model != None)
    assert(attacker != None)
    assert(target != None)
    assert(dice != None)

    ac = get_armour_class(model, target)
    if len(dice) > 0:
        attackRoll = dice.pop() + get_melee_attack_bonus(model, attacker)
    else:
        attackRoll = random.randint(1, 20) + get_melee_attack_bonus(model, attacker)

    if attackRoll >= ac:
        return 1
    else:
        return 0

def get_damage_in_melee(model, attacker, target, dice = []):
    """
    Gets damage done in melee
    @param model: model of the world
    @param attacker: character attacking
    @param target: target of the attack
    @param dice: optional prerolled dice
    """
    assert(model != None)
    assert(attacker != None)
    assert(target != None)
    assert(dice != None)

    damage = Damage()

    if len(attacker.weapons) > 0:
        #use weapon in close combat attack
        if hasattr(attacker.weapons[0], 'damage'):
            attackDice = attacker.weapons[0].damage
        else:
            #mundane items do 1 point of damage + bonuses
            attackDice = '1d1'
    else:
        #attack with bare hands
        attackDice = attacker.attack

    if len(dice) > 0:
        damageRoll = dice.pop()
        assert(damageRoll <= utils.getMaxScore(attackDice))
    else:
        damageRoll = utils.rollDice(attackDice)

    if len(attacker.weapons) > 0:
        weapon = attacker.weapons[0]
        if hasattr(weapon, 'tags'):
            if 'light weapon' in weapon.tags:
                #light weapons get only 1 * str bonus when wielded two-handed
                damage.amount = damageRoll + get_attribute_modifier(model, attacker, 'str')
                damage.type = weapon.damageType
            else:
                #all other melee weapons get 1.5 * str bonus when wielded two-handed
                damage.amount = damageRoll + get_attribute_modifier(model, attacker, 'str') * 1.5
                damage.type = weapon.damageType
        else:
            #character is using a mundane item as a weapon
            damage.amount = damageRoll + get_attribute_modifier(model, attacker, 'str')
            damage.type = 'bludgeoning'
    else:
        #unarmed combat get only 1 * str bonus
        damage.amount = damageRoll + get_attribute_modifier(model, attacker, 'str')
        damage.type = 'bludgeoning'

    damage.amount = int(round(damage.amount))
    if damage.amount < 1:
        damage.amount = 1
    return damage

def get_melee_attack_bonus(model, character):
    """
    Get attack bonus used in melee
    @param model: model of the world
    @param character: character whose attack bonus should be calculated
    @return: Attack bonus
    """
    return  get_attribute_modifier(model, character, 'str') + get_size_modifier(model, character)

def get_armour_class(model, character):
    """
    Get armour class of character
    @param model: model of the world
    @param character: character whose armour class should be calculated
    @return: Armour class
    """
    return 10 + get_size_modifier(model, character) + get_attribute_modifier(model, character, 'dex')

def get_attribute_modifier(model, character, attribute):
    """
    Get attribute modifier
    @param model: model of the world
    @param character: character whose attribute modifier should be calculated
    @param attribute: attribute to check
    @note: valid attributes are: str, dex
    @return: Attribute modifier
    """
    assert(model != None)
    assert(character != None)

    if attribute == 'str':
        return model.tables.attributeModifier[character.str]
    elif attribute == 'dex':
        return model.tables.attributeModifier[character.dex]

def get_size_modifier(model, character):
    """
    Get size modifier for character
    @param model: model of the world
    @param character: character whose size modifier should be calculated
    """
    assert(model != None)
    assert(character != None)

    return model.tables.sizeModifier[character.size]


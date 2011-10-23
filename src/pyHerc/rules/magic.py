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

import os, sys
import logging
import pyHerc.data.model
import pyHerc.rules.utils

__logger = logging.getLogger('pyHerc.rules.magic')

def cast_effect(model, target, effect, dice = None):
    """
    Casts effect of a spell, potion, etc. on a target
    @param model: model to use
    @param target: target of the effect
    @param effect: ItemEffectData object
    @param dice: prerolled dice
    """
    assert(effect != None)

    __logger.info('casting effect: ' + effect.effect_type)

    if effect.effect_type in ('healing', 'damage'):
        cast_hp_effect(model, target, effect, dice)

def cast_hp_effect(model, target, effect, dice = None):
    """
    Casts HP effect on target, causing it to gain or lose some HP
    @param model: model to use
    @param target: target of the effect
    @param effect: parameters of effect in dictionary
    @param dice: prerolled dice
    """
    hpPower = effect.power
    if dice != None and len(dice) > 0:
        hpRoll = dice.pop()
        assert(hpRoll <= pyHerc.rules.utils.get_max_score(hpPower))
    else:
        hpRoll = pyHerc.rules.utils.roll_dice(hpPower)

    event = {}

    if effect.effect_type == 'healing':
        target.hp = target.hp + hpRoll
        event['type'] = 'magic heal'
    elif effect.effect_type == 'damage':
        target.hp = target.hp - hpRoll
        event['type'] = 'magic damage'

    if target.hp < 0:
        pyHerc.rules.ending.check_dying(model, target, None)

    if target.hp > target.get_max_HP():
        target.hp = target.get_max_HP()

    event['character'] = target
    event['location'] = target.location
    event['level'] = target.level
    event['power'] = hpRoll

    model.raise_event(event)

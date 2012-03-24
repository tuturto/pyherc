#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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
Module for magic
"""

import logging
import pyherc.data.model
import pyherc.rules.utils

__logger = logging.getLogger('pyherc.rules.magic')

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
    hp_power = effect.power
    if dice != None and len(dice) > 0:
        hp_roll = dice.pop()
        assert(hp_roll <= pyherc.rules.utils.get_max_score(hp_power))
    else:
        hp_roll = pyherc.rules.utils.roll_dice(hp_power)

    event = {}

    if effect.effect_type == 'healing':
        target.hit_points = target.hit_points + hp_roll
        event['type'] = 'magic heal'
    elif effect.effect_type == 'damage':
        target.hit_points = target.hit_points - hp_roll
        event['type'] = 'magic damage'

    if target.hit_points < 0:
        pyherc.rules.ending.check_dying(model, target, None)

    if target.hit_points > target.get_max_hp():
        target.hit_points = target.get_max_hp()

    event['character'] = target
    event['location'] = target.location
    event['level'] = target.level
    event['power'] = hp_roll

    if model != None:
        model.raise_event(event)

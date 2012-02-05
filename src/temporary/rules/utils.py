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

import os, sys
import logging
import random

__logger = logging.getLogger('pyherc.rules.utils')

def roll_dice(dice):
    """
    Roll dice
    @param dice: dice to roll, in format AdS+B
    @return: rolled score
    """
    assert(dice.count('d') == 1)

    score = 0

    amount, d, parts = dice.partition('d')

    if parts.count('+') == 1:
        sides, sign, bonus = parts.partition('+')
    else:
        sides, sign, bonus = parts.partition('-')

    for i in range(0, int(amount)):
        score = score + random.randint(1, int(sides))

    if sign == '+':
        score = score + int(bonus)
    elif sign == '-':
        score = score - int(bonus)

    return score

def get_max_score(dice):
    """
    Get maximum score possible with given dice
    @param dice: dice to roll, in format AdS+B
    @return: maximum score
    """
    assert(dice.count('d') == 1)

    score = 0

    amount, d, parts = dice.partition('d')

    if parts.count('+') == 1:
        sides, sign, bonus = parts.partition('+')
    else:
        sides, sign, bonus = parts.partition('-')

    for i in range(0, int(amount)):
        score = score + int(sides)

    if sign == '+':
        score = score + int(bonus)
    elif sign == '-':
        score = score - int(bonus)

    return score

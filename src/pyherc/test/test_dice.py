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
Module for testing dice
"""

import pyherc
import pyherc.rules.utils

class TestDice(object):
    '''
    Test rolling dice
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def test_simple_die_rolling(self):
        '''
        Test that single d6 rolls are between 1 and 6
        '''
        for i in range(0, 50):
            score = pyherc.rules.utils.roll_dice('1d6')
            assert(score >= 1)
            assert(score <= 6)

    def test_multiple_dice_rolls(self):
        '''
        Test that 2d6 rolls are between 2 and 12
        '''
        for i in range(0, 50):
            score = pyherc.rules.utils.roll_dice('2d6')
            assert(score >= 2)
            assert(score <= 12)

    def test_multiple_dice_rolls_with_bonus(self):
        '''
        Test that 2d6+2 rolls are between 4 and 14
        '''
        for i in range(0, 50):
            score = pyherc.rules.utils.roll_dice('2d6+2')
            assert(score >= 4)
            assert(score <= 14)

    def test_multiple_dice_rolls_with_penalty(self):
        '''
        Test that negative penalties are applied to rolls
        '''
        for i in range(0, 50):
            score = pyherc.rules.utils.roll_dice('4d4-3')
            assert(score >= 1)
            assert(score <= 13)

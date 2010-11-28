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

import pyHerc
import pyHerc.rules.utils

class test_dice:

    def test_simpleDieRolling(self):
        for i in range(0, 50):
            score = pyHerc.rules.utils.rollDice('1d6')
            assert(score >= 1)
            assert(score <= 6)

    def test_multipleDiceRolls(self):
        for i in range(0, 50):
            score = pyHerc.rules.utils.rollDice('2d6')
            assert(score >= 2)
            assert(score <= 12)

    def test_multipleDiceRollsWithBonus(self):
        for i in range(0, 50):
            score = pyHerc.rules.utils.rollDice('2d6+2')
            assert(score >= 4)
            assert(score <= 14)

    def test_multipleDiceRollsWithPenalty(self):
        for i in range(0, 50):
            score = pyHerc.rules.utils.rollDice('4d4-3')
            assert(score >= 1)
            assert(score <= 13)

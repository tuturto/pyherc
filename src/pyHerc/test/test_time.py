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
import pyHerc.rules.time
from pyHerc.data.model import Model
from pyHerc.data.model import Character
from pyHerc.data.dungeon import Dungeon
from pyHerc.data.dungeon import Level


class test_Time:

    def setup(self):
        self.creature1 = Character(None)
        self.creature2 = Character(None)
        self.creature3 = Character(None)

        self.model = Model()
        self.model.dungeon = Dungeon()
        self.model.dungeon.levels = Level((20, 20), 0, 0)

        self.creature1.tick = 5
        self.creature1.speed = 1
        self.creature1.name = 'creature 1'
        self.creature2.tick = 0
        self.creature2.speed = 2
        self.creature2.name = 'creature 2'
        self.creature3.tick = 3
        self.creature3.speed = 0.5
        self.creature3.name = 'creature 3'

        self.model.dungeon.levels.add_creature(self.creature1)
        self.model.dungeon.levels.add_creature(self.creature2)
        self.model.player = self.creature3
        self.creature3.level = self.model.dungeon.levels

    def test_getNextInTurnZeroTick(self):
        """
        Test that system can tell whose turn it is to act
        One creature has tick of 0
        """
        creature = pyHerc.rules.time.get_next_creature(self.model)
        assert(creature == self.creature2)

    def test_getNextInTurnPositiveTick(self):
        """
        Test that system can tell whose turn it is to act
        All creatures have positive tick
        """
        self.creature2.tick = 10
        creature = pyHerc.rules.time.get_next_creature(self.model)
        print creature
        assert(creature == self.creature3)


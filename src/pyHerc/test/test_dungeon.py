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
from pyHerc.data.dungeon import Level
from pyHerc.data.dungeon import Portal
from pyHerc.data import tiles

class test_dungeon:

    def test_simple_level_creation(self):
        level = Level([20, 20], tiles.floor_rock, tiles.wall_empty)
        assert not (level is None)
        assert (level.floor[5][5] == tiles.floor_rock)
        assert(level.walls[0][0] == tiles.wall_empty)

    def test_StairLinking(self):
        level1 = Level([20, 20], tiles.floor_rock, tiles.wall_empty)
        level2 = Level([20, 20], tiles.floor_rock, tiles.wall_empty)

        stairs1 = Portal()
        stairs1.icon = tiles.portal_stairs_down
        level1.addPortal(stairs1, (10, 10))

        stairs2 = Portal()
        level2.addPortal(stairs2, (5, 5), stairs1)

        assert(stairs1.level == level1)
        assert(stairs1.location == (10, 10))
        assert(stairs1.getOtherEnd() == stairs2)

        assert(stairs2.level == level2)
        assert(stairs2.location == (5, 5))
        assert(stairs2.getOtherEnd() == stairs1)

        assert(stairs1 in level1.portals)
        assert(stairs2 in level2.portals)

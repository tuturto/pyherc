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

from pyherc.data.dungeon import Level
from pyherc.data.dungeon import Portal
from pyherc.data import tiles

class test_dungeon:

    def test_simple_level_creation(self):
        level = Level([20, 20], tiles.FLOOR_ROCK, tiles.WALL_EMPTY)
        assert not (level is None)
        assert (level.floor[5][5] == tiles.FLOOR_ROCK)
        assert(level.walls[0][0] == tiles.WALL_EMPTY)

    def test_StairLinking(self):
        level1 = Level([20, 20], tiles.FLOOR_ROCK, tiles.WALL_EMPTY)
        level2 = Level([20, 20], tiles.FLOOR_ROCK, tiles.WALL_EMPTY)

        stairs1 = Portal()
        stairs1.icon = tiles.PORTAL_STAIRS_DOWN
        level1.add_portal(stairs1, (10, 10))

        stairs2 = Portal()
        level2.add_portal(stairs2, (5, 5), stairs1)

        assert(stairs1.level == level1)
        assert(stairs1.location == (10, 10))
        assert(stairs1.get_other_end() == stairs2)

        assert(stairs2.level == level2)
        assert(stairs2.location == (5, 5))
        assert(stairs2.get_other_end() == stairs1)

        assert(stairs1 in level1.portals)
        assert(stairs2 in level2.portals)

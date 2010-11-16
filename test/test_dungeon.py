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
from pyHerc.data import tiles

class test_dungeon:

    def test_simple_level_creation(self):
        level = Level([20, 20], tiles.floor_rock, tiles.wall_empty)
        assert not (level is None)
        assert (level.floor[5][5] == tiles.floor_rock)
        assert(level.walls[0][0] == tiles.wall_empty)

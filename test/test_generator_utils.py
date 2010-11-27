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
import pyHerc.generators.utils

class test_generatorUtils:

    def test_simpleBSPSplit_horisontal(self):
        section = pyHerc.generators.utils.BSPSection((0, 0), (20, 20), None)
        assert(section.node1 == None)
        assert(section.node2 == None)

        section.split(direction = 1)
        # 1 split horisontal
        # 2 split vertical

        assert(section.node1 != None)
        assert(section.node2 != None)

        assert(section.node1.corner1[0] == section.node2.corner1[0])
        assert(section.node1.corner1[1] == 0)
        assert(section.node1.corner2[0] == 20)
        assert(section.node1.corner2[1] == section.node2.corner1[1] -1)
        assert(section.node2.corner2[0] == 20)
        assert(section.node2.corner2[1] == 20)

    def test_simpleBSPSplit_vertical(self):
        section = pyHerc.generators.utils.BSPSection((0, 0), (20, 20), None)
        assert(section.node1 == None)
        assert(section.node2 == None)

        section.split(direction = 2)
        # 1 split horisontal
        # 2 split vertical

        assert(section.node1 != None)
        assert(section.node2 != None)

        assert(section.node1.corner1[0] == 0)
        assert(section.node1.corner1[1] == 0)
        assert(section.node1.corner2[0] == section.node2.corner1[0] - 1)
        assert(section.node1.corner2[1] == 20)
        assert(section.node2.corner2[0] == 20)
        assert(section.node2.corner2[1] == 20)

    def test_simpleBSPSplit_notEnoughSpace(self):
        section = pyHerc.generators.utils.BSPSection((0, 0), (10, 10), None)
        assert(section.node1 == None)
        assert(section.node2 == None)

        section.split()

        assert(section.node1 == None)
        assert(section.node2 == None)


#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Module for testing generator utilities
"""

import pyherc
import pyherc.generators.utils

class TestGeneratorUtils():
    """
    Tests for generator utilities
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_simpleBSPSplit_horizontal(self):
        """
        Test that BSP section can be split horizontally
        """
        section = pyherc.generators.utils.BSPSection((0, 0), (20, 20), None)
        assert(section.node1 == None)
        assert(section.node2 == None)

        section.split(direction = 1)
        # 1 split horizontal
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
        """
        Test that bsp section can split vertical
        """
        section = pyherc.generators.utils.BSPSection((0, 0), (20, 20), None)
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
        """
        Test that bsp split does not try to split when there is not enough space
        """
        section = pyherc.generators.utils.BSPSection((0, 0), (10, 10), None)
        assert(section.node1 == None)
        assert(section.node2 == None)

        section.split()

        assert(section.node1 == None)
        assert(section.node2 == None)

    def test_getAreaQueue(self):
        """
        Test basic functionality of area queue
        """
        section1 = pyherc.generators.utils.BSPSection((0, 0), (20, 20), None)
        section2 = pyherc.generators.utils.BSPSection((0, 0), (20, 10), None)
        section3 = pyherc.generators.utils.BSPSection((0, 11), (20, 20), None)
        section1.node1 = section2
        section1.node2 = section3
        section3.parent = section1
        section2.parent = section1
        section4 = pyherc.generators.utils.BSPSection((0, 0), (10, 10), None)
        section5 = pyherc.generators.utils.BSPSection((11, 0), (20, 10), None)
        section2.node1 = section4
        section2.node2 = section5
        section4.parent = section2
        section5.parent = section2

        queue = section1.get_area_queue()

        assert(queue.pop() == section1)
        assert(queue.pop() in (section2, section3))
        assert(queue.pop() in (section2, section3))
        assert(queue.pop() in (section4, section5))
        assert(queue.pop() in (section4, section5))


# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
        assert(section.node1 is None)
        assert(section.node2 is None)

        section.split(direction = 1)
        # 1 split horizontal
        # 2 split vertical

        assert(section.node1 is not None)
        assert(section.node2 is not None)

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
        assert(section.node1 is None)
        assert(section.node2 is None)

        section.split(direction = 2)
        # 1 split horisontal
        # 2 split vertical

        assert(section.node1 is not None)
        assert(section.node2 is not None)

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
        assert(section.node1 is None)
        assert(section.node2 is None)

        section.split()

        assert(section.node1 is None)
        assert(section.node2 is None)

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

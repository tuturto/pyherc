#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
Tests for Section
"""
#pylint: disable=W0614
from pyherc.generators.level.partitioners.section import Section
from hamcrest import * #pylint: disable=W0401

class TestSectionCalculations(object):
    """
    Tests for sections methods
    """
    def __init__(self):
        """
        Default constructor
        """
        self.section = None

    def setup(self):
        """
        Setup test case
        """
        self.section = Section((10, 10), (20, 25))

    def test_left_edge(self):
        """
        Test that left edge can be calculated correctly
        """
        left_edge = self.section.left_edge
        assert_that(left_edge, is_(equal_to(10)))

    def test_top_edge(self):
        """
        Test that top edge can be calculated correctly
        """
        top_edge = self.section.top_edge
        assert_that(top_edge, is_(equal_to(10)))

    def test_width(self):
        """
        Test that width can be calculated correctly
        """
        width = self.section.width
        assert_that(width, is_(equal_to(10)))

    def test_height(self):
        """
        Test that height can be calculated correctly
        """
        height = self.section.height
        assert_that(height, is_(equal_to(15)))

    def test_border(self):
        """
        Test that Section can report border
        """
        border = self.section.get_border()
        assert_that(border, has_items(
                            (10, 10), (11, 10), (12, 10), (19, 10), (20, 10),
                            (10, 11), (10, 12), (10, 13), (10, 24), (10, 25),
                            (11, 25), (12, 25), (13, 25), (19, 25), (20, 25),
                            (20, 11), (20, 12), (20, 13), (20, 23), (20, 24),
                            ))

class TestSectionConnections(object):
    """
    Class for testing Section
    """
    def __init__(self):
        """
        Default constructor
        """
        self.section1 = None
        self.section2 = None

    def setup(self):
        """
        Setup test case
        """
        self.section1 = Section((0, 0), (10, 20))
        self.section2 = Section((11, 0), (20, 20))

        self.section1.neighbours.append(self.section2)
        self.section2.neighbours.append(self.section1)

    def test_unconnected_neighbours(self):
        """
        Test that unconnected neighbours can be detected
        """
        assert_that(self.section1.has_unconnected_neighbours())

    def test_connected_neighbours_are_not_reported(self): #pylint: disable=C0103
        """
        Test that connected neighbours are not reported as unconnected
        """
        self.section1.connect_to(self.section2)

        assert_that(is_not(self.section1.has_unconnected_neighbours()))

    def test_section_connection_points(self):
        """
        Test that linked sections have their connection points set up
        so that they line up in the border
        """
        self.section1.connect_to(self.section2)

        point1 = self.section1.connections[0]
        point2 = self.section2.connections[0]

        assert_that(point1.location[0], is_(equal_to(10)))
        assert_that(point2.location[0], is_(equal_to(11)))
        assert_that(point1.location[1], is_(equal_to(point2.location[1])))

    def test_get_common_border(self):
        """
        Test that Section can calculate common border with another Section
        """
        common_border = self.section1.get_common_border(self.section2)

        assert_that(common_border, contains_inanyorder(
                                        (10, 0), (10, 1), (10, 2), (10, 3),
                                        (10, 4), (10, 5), (10, 6), (10, 7),
                                        (10, 8), (10, 9), (10, 10), (10, 11),
                                        (10, 12), (10, 13), (10, 14), (10, 15),
                                        (10, 16), (10, 17), (10, 18), (10, 19),
                                        (10, 20)))

    def test_get_opposing_point(self):
        """
        Test that Section can calculate which of its points corresponds to the
        point given on the other side of the border
        """
        my_point = (10, 9)
        other_point = self.section2.get_opposing_point(my_point)

        assert_that(other_point, is_(equal_to((11, 9))))

    def test_adding_room_connections(self):
        """
        Test that added room connections are kept track
        """
        self.section1.add_room_connection((5, 5), "right")

        assert_that(self.section1.room_connections, has_length(1))

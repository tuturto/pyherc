# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
import random

from hamcrest import (assert_that,  # pylint: disable-msg=E0611; pylint: disable-msg=E0611
                      contains_inanyorder, equal_to, has_items, has_length, is_,
                      is_not)
from mockito import mock
from pyherc.data import Level, floor_tile
from pyherc.generators.level.partitioners.section import Section


class TestSectionCalculations():
    """
    Tests for sections methods
    """
    def __init__(self):
        """
        Default constructor
        """
        self.section = None
        self.rng = None

    def setup(self):
        """
        Setup test case
        """
        mock_level = mock(Level)
        self.rng = random.Random()
        self.section = Section((10, 10), (20, 25), mock_level, self.rng)

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
                            (11, 10, "down"), (12, 10, "down"),
                            (18, 10, "down"), (19, 10, "down"),
                            (10, 11, "right"), (10, 12, "right"),
                            (10, 23, "right"), (10, 24, "right"),
                            (11, 25, "up"), (12, 25, "up"),
                            (18, 25, "up"), (19, 25, "up"),
                            (20, 11, "left"), (20, 12, "left"),
                            (20, 23, "left"), (20, 24, "left"),
                            ))

class TestSectionConnections():
    """
    Class for testing Section
    """
    def __init__(self):
        """
        Default constructor
        """
        self.section1 = None
        self.section2 = None
        self.rng = random.Random()

    def setup(self):
        """
        Setup test case
        """
        mock_level = mock(Level)
        self.section1 = Section((0, 0), (10, 20), mock_level, self.rng)
        self.section2 = Section((11, 0), (20, 20), mock_level, self.rng)

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

    def test_section_connections_have_direction(self):
        """
        Test that connections between sections have their directions set up
        """
        self.section1.connect_to(self.section2)

        point1 = self.section1.connections[0]
        point2 = self.section2.connections[0]

        assert_that(point1.direction, is_(equal_to("left")))
        assert_that(point2.direction, is_(equal_to("right")))

    def test_get_common_border(self):
        """
        Test that Section can calculate common border with another Section
        """
        common_border = self.section1.get_common_border(self.section2)

        assert_that(common_border, contains_inanyorder(
                                        (10, 1, "left"), (10, 2, "left"),
                                        (10, 3, "left"), (10, 4, "left"),
                                        (10, 5, "left"), (10, 6, "left"),
                                        (10, 7, "left"), (10, 8, "left"),
                                        (10, 9, "left"), (10, 10, "left"),
                                        (10, 11, "left"), (10, 12, "left"),
                                        (10, 13, "left"), (10, 14, "left"),
                                        (10, 15, "left"), (10, 16, "left"),
                                        (10, 17, "left"), (10, 18, "left"),
                                        (10, 19, "left"),
                                        ))

    def test_get_opposing_point(self):
        """
        Test that Section can calculate which of its points corresponds to the
        point given on the other side of the border
        """
        my_point = (10, 9)
        other_point = self.section2.get_opposing_point(my_point)

        assert_that(other_point, is_(equal_to((11, 9, "right"))))

    def test_adding_room_connections(self):
        """
        Test that added room connections are kept track
        """
        self.section1.add_room_connection((5, 5), "right")

        assert_that(self.section1.room_connections, has_length(1))

    def test_finding_room_connection(self):
        """
        Test that room connection can be found for given section connection
        """
        self.section1.add_room_connection((7, 5), "right")
        self.section1.add_room_connection((3, 5), "left")
        self.section1.add_room_connection((5, 7), "down")
        self.section1.add_room_connection((5, 3), "right")

        self.section1.connect_to(self.section2)
        edge_connection = self.section1.connections[0]

        connection = self.section1.find_room_connection(edge_connection)

        assert_that(connection.direction, is_(equal_to("right")))

class TestSectionLevelAccess():
    """
    Tests to ensure that client has access to portion of level via Section
    """
    def __init__(self):
        """
        Default constructor
        """
        object.__init__(self)
        self.level = None
        self.section = None
        self.floor_empty = None
        self.floor_rock = None
        self.wall_empty = None
        self.wall_ground = None
        self.rng = random.Random()

    def setup(self):
        """
        Setup the test case
        """
        self.floor_empty = 0
        self.floor_rock = 1
        self.wall_empty = 10
        self.wall_ground = 11
        self.level = Level(mock(), (10, 10), self.floor_empty, self.wall_empty)
        self.section = Section((0, 0), (10, 10), self.level, self.rng)

    def test_setting_floor(self):
        """
        Test that floor can be set
        """
        self.section.set_floor((5, 5), self.floor_rock, None)

        assert_that(floor_tile(self.level, (5, 5)),
                    is_(equal_to(self.floor_rock)))

    def test_setting_wall(self):
        """
        Test that walls can be set
        """
        self.section.set_wall((2, 2), self.wall_ground, None)

        assert_that(self.level.walls[2][2], is_(equal_to(self.wall_ground)))

    def test_setting_location_type(self):
        """
        Test that location type can be set correctly
        """
        self.section.set_floor((2, 3), self.floor_rock, 'corridor')

        assert_that(self.level.get_location_type((2, 3)),
                                    is_(equal_to('corridor')))

class TestSectionLevelAccessWithOffset():
    """
    Tests to ensure that client has access to portion of level via Section that
    has been offset from the level
    """
    def __init__(self):
        """
        Default constructor
        """
        object.__init__(self)
        self.level = None
        self.section = None
        self.rng = random.Random()
        self.floor_empty = None
        self.floor_rock = None
        self.wall_empty = None
        self.wall_ground = None

    def setup(self):
        """
        Setup the test case
        """
        self.floor_empty = 0
        self.floor_rock = 1
        self.wall_empty = 10
        self.wall_ground = 11
        self.level = Level(mock(), (10, 10), self.floor_empty, self.wall_empty)
        self.section = Section((5, 5), (10, 10), self.level, self.rng)

    def test_setting_floor_with_offset(self):
        """
        Test that off set Section is correctly mapped to the level
        """
        self.section.set_floor((2, 2), self.floor_rock, None)

        assert_that(floor_tile(self.level, (7, 7)),
                    is_(equal_to(self.floor_rock)))

    def test_setting_wall_with_offset(self):
        """
        Test that offset Section is correctly mapped to the level
        """
        self.section.set_wall((3, 2), self.wall_ground, None)

        assert_that(self.level.walls[8][7], is_(equal_to(self.wall_ground)))

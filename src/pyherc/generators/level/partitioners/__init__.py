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

# flake8: noqa

"""
Package for level partitioners and related classes
"""

from .binary import binary_space_partitioning
from .old_grid import RandomConnector
from .grid import grid_partitioning
from .section import section_corners, section_width, section_height
from .section import left_edge, right_edge, top_edge, bottom_edge
from .section import section_to_map, section_floor, section_wall
from .section import section_ornamentation, section_trap
from .section import section_connections, room_connections
from .section import add_section_connection, add_room_connection
from .section import is_connected, neighbour_sections
from .section import mark_neighbours, unconnected_neighbours
from .section import is_unconnected_neighbours
from .section import section_border, common_border, opposing_point
from .section import match_section_to_room, section_location_tag
from .section import connect_sections, section_level, section_data
from .section import mark_all_neighbours, is_equal_sections, is_section_in
from .section import Connection
from .section import new_section
from .section import connected_left, connected_right, connected_up
from .section import connected_down, is_adjacent_sections

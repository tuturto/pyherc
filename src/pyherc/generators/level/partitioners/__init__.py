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

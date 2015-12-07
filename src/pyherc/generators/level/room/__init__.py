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
Package for room generators
"""

from .areas import (center_tile, random_columns, random_rows, center_area,
                    random_pillars)
from .areas import side_by_side
from .corridor import corridors
from .cache import CacheRoomGenerator, cache_creator
from .circle import CircularRoomGenerator, TempleRoomGenerator
from .squareroom import SquareRoomGenerator
from .pillarroom import PillarRoomGenerator
from .catacombs import CatacombsGenerator
from .crimson_lair import CrimsonLairGenerator
from .library import LibraryRoomGenerator
from .overlays import add_rows, add_columns, mark_center_area
from .generator import new_room_generator
from .shapes import square_shape, circular_shape
from .traps import trap_creator
from .walls import wall_creator, floor_creator, ornament_creator

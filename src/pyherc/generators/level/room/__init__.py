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
Package for room generators
"""

from .areas import center_tile, random_columns, random_rows, center_area
from .corridor import corridors
from .cache import CacheRoomGenerator, cache_creator
from .circle import CircularRoomGenerator, TempleRoomGenerator
from .squareroom import SquareRoomGenerator
from .pillarroom import PillarRoomGenerator
from .catacombs import CatacombsGenerator
from .crimson_lair import CrimsonLairGenerator
from .pitroom import PitRoomGenerator
from .library import LibraryRoomGenerator
from .overlays import add_rows, add_columns, mark_center_area
from .generator import new_room_generator
from .shapes import square_shape, circular_shape
from .traps import trap_creator

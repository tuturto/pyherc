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
Module for data related modules and classes that represent state of the game
"""
from .dungeon import Dungeon
from .portal import Portal

from .model import Model

from .character import Character
from .character import WeaponProficiency

from .item import Item
from .new_item import (is_weapon, is_armour, is_potion, is_ammunition,
                       is_food, is_trap_bag, is_boots)

from .constants import Duration, SpecialTime, Direction

from .geometry import distance_between, heuristic_estimate_of_distance
from .geometry import area_4_around, area_around, find_direction

from .new_character import (is_skill_ready, cooldown, add_visited_level, visited_levels,
                            speed_modifier, movement_mode)
from .level import (get_tile, new_tile, floor_tile, add_portal, get_portal,
                    wall_tile, tile, blocks_los, ornamentation,
                    level_size, find_free_space, blocks_movement,
                    add_item, get_items, remove_item,
                    add_character, remove_character, get_character,
                    get_characters,
                    move_character, add_trap, get_traps, remove_trap,
                    add_location_tag, get_location_tags, get_locations_by_tag,
                    new_level, get_tiles,
                    location_features, add_location_feature,
                    remove_location_feature,
                    level_name, level_description, safe_passage)
from .locations import is_next_to_wall, is_corridor, is_open_area

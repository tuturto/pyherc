# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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
                            speed_modifier)
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

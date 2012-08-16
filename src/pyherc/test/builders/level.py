#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module for level builder
"""
from pyherc.data import Level

class LevelBuilder(object):
    """
    Class for building levels
    """
    def __init__(self):
        """
        Default constructor
        """
        super(LevelBuilder, self).__init__()
        self.characters = []
        self.level_size = (80, 40)
        self.floor_tile = 1
        self.wall_tile = 10
        self.empty_wall_tile = 10
        self.solid_wall_tile = 11
        self.walls = []

    def with_floor_tile(self, tile):
        self.floor_tile = tile
        return self

    def with_wall_tile(self, tile):
        self.wall_tile = tile
        return self

    def with_empty_wall_tile(self, tile):
        self.empty_wall_tile = tile
        return self

    def with_solid_wall_tile(self, tile):
        self.solid_wall_tile = tile
        return self

    def with_character(self, character, location = None):
        """
        Place given character to level

        :param character: character to place to level
        :type character: Character
        """
        if hasattr(character, 'build'):
            new_character = character.build()
        else:
            new_character = character

        if location != None:
            new_character.location = location

        self.characters.append(new_character)
        return self

    def with_wall_at(self, location):
        """
        Place wall to given location

        :param location: location of the wall
        :type location: (int, int)
        """
        self.walls.append(location)
        return self

    def build(self):
        """
        Build level

        Returns:
            Level
        """
        level = Level(size = self.level_size,
                      floor_type = self.floor_tile,
                      wall_type = self.wall_tile,
                      empty_wall = self.empty_wall_tile)

        for wall in self.walls:
            level.walls[wall[0]][wall[1]] = self.solid_wall_tile

        for creature in self.characters:
            level.add_creature(creature)

        return level

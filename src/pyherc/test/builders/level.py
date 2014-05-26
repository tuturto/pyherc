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
Module for level builder
"""
from pyherc.data import Level, Model, wall_tile, add_character


class LevelBuilder():
    """
    Class for building levels
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.characters = []
        self.level_size = (80, 40)
        self.floor_tile = 1
        self.wall_tile = None
        self.empty_wall_tile = None
        self.solid_wall_tile = 11
        self.walls = []
        self.model = Model()

    def with_model(self, model):
        self.model = model
        return self

    def with_floor_tile(self, tile):
        self.floor_tile = tile
        return self

    def with_wall_tile(self, tile):
        self.wall_tile = tile
        return self

    def with_solid_wall_tile(self, tile):
        self.solid_wall_tile = tile
        return self

    def with_character(self, character, location=None):
        """
        Place given character to level

        :param character: character to place to level
        :type character: Character
        """
        if hasattr(character, 'build'):
            new_character = character.build()
        else:
            new_character = character

        if location is not None:
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

    def with_size(self, size):
        """
        Configure size
        """
        self.level_size = size
        return self

    def build(self):
        """
        Build level

        Returns:
            Level
        """
        level = Level(model=self.model,
                      size=self.level_size,
                      floor_type=self.floor_tile,
                      wall_type=self.wall_tile)

        for wall in self.walls:
            wall_tile(level, wall, self.solid_wall_tile)

        for creature in self.characters:
            add_character(level, creature.location, creature)

        return level

# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
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

"""
Module for level builder
"""
from pyherc.data import new_level, Model, wall_tile, floor_tile, add_character


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
        self.level_size = (10, 10)
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
        level = new_level(self.model)

        for x_loc in range(self.level_size[0]):
            for y_loc in range(self.level_size[1]):
                wall_tile(level, (x_loc, y_loc), self.wall_tile)
                floor_tile(level, (x_loc, y_loc), self.floor_tile)

        for wall in self.walls:
            wall_tile(level, wall, self.solid_wall_tile)

        for creature in self.characters:
            add_character(level, creature.location, creature)

        return level

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
from pyherc.data import tiles

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
        self.floor_tile = tiles.FLOOR_ROCK
        self.wall_tile = tiles.WALL_EMPTY

    def with_character(self, character):
        if hasattr(character, 'build'):
            self.characters.append(character.build())
        else:
            self.characters.append(character)
        return self

    def build(self):
        """
        Build level

        Returns:
            Level
        """
        level = Level(self.level_size, self.floor_tile, self.wall_tile)

        for creature in self.characters:
            level.add_creature(creature)

        return level

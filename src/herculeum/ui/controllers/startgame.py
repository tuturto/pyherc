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
Module for starting game
"""
from pyherc.generators import DungeonGenerator
from pyherc.aspects import log_debug


class StartGameController():
    """
    """
    @log_debug
    def __init__(self, level_generator_factory,
                 creature_generator, item_generator, start_level):
        """
        Default constructor
        """
        super().__init__()

        self.level_generator_factory = level_generator_factory
        self.creature_generator = creature_generator
        self.item_generator = item_generator
        self.start_level = start_level

    @log_debug
    def setup_world(self, world, player):
        """
        Setup playing world
        """
        world.player = player
        level_generator = self.level_generator_factory.get_generator(self.start_level)  # noqa

        generator = DungeonGenerator(self.creature_generator,
                                     self.item_generator,
                                     level_generator)

        generator.generate_dungeon(world)
        world.level = world.dungeon.levels

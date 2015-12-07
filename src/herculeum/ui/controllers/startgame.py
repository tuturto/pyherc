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

"""
Module for starting game
"""
from pyherc.aspects import log_debug
from pyherc.generators import generate_dungeon


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

        world.dungeon = generate_dungeon(world, level_generator)
        world.level = world.dungeon.levels

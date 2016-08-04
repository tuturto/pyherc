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
import random

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

        return self.generate_intro_text()

    def generate_intro_text(self):
        """
        Generate short intro text
        """
        first_line = random.choice(["After double checking your gear,",
                                    "Remembering wise words of your father,",
                                    "Remembering wisdom of your mother,",
                                    "Eager to start,",
                                    "Tired from long journey,",
                                    "Thinking of your pet kakadu,",
                                    "Worried about the dangers ahead,",
                                    "After traveling for days,",
                                    "After crossing the divide of Kadurr,",
                                    "Avoiding subterranean dangers,",
                                    "Sneaking past first traps,",
                                    "Breaking your camp,",
                                    "Leaving unneccessary items behind,"])

        second_line = random.choice(["you consulted the map once more,",
                                     "you finished your meal,",
                                     "you recited the rites of labyrinth",
                                     "you contemplated silently,",
                                     "you whistled nervously,",
                                     "you offered a silent prayer,",
                                     "you felt ready for anything,",
                                     "you tightened your belt,",
                                     "you adjusted your clothes,",
                                     "you paid your dungeon guide,"])

        third_line = random.choice(["and prepared for long ascent.",
                                    "and started your ascent.",
                                    "and looked back one last time.",
                                    "and tossed away your broken clock.",
                                    "and checked your bearings.",
                                    "and remembered time past.",
                                    "and looked forward for adventure.",
                                    "and could swear that somebody was watching you.",
                                    "and had a bad feeling about this.",
                                    "and prepared for worst.",
                                    "and checked that your shoes were in correct feet.",
                                    "and felt tingling at your back."])

        return "\n".join([first_line, second_line, third_line])


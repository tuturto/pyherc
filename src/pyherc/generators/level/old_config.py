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
Classes for configuring level generation
"""
from pyherc.aspects import log_debug


class LevelGeneratorFactoryConfig():
    """
    Class to configure level generator
    """
    @log_debug
    def __init__(self, room_generators, level_partitioners,
                 decorators, item_adders, creature_adders,
                 portal_adder_configurations, contexts, model):
        """
        Default constructor
        """
        super().__init__()
        self.room_generators = room_generators
        self.level_partitioners = level_partitioners
        self.decorators = decorators
        self.item_adders = item_adders
        self.creature_adders = creature_adders
        self.portal_adder_configurations = portal_adder_configurations
        self.contexts = contexts
        self.model = model

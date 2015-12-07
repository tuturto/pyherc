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
module for LevelGeneratorFactoryConfig
"""
from pyherc.generators.level.old_config import LevelGeneratorFactoryConfig


class LevelConfiguration():
    """
    DSL for configuring levels
    """

    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.room_generators = None
        self.level_partitioners = None
        self.decorators = None
        self.item_adders = None
        self.creature_adders = None
        self.portal_adder_configurations = None
        self.contexts = None
        self.model = None

    def with_model(self, model):
        """
        set model to use
        """
        self.model = model
        return self

    def with_contexts(self, contexts):
        """
        Set level contexts which specify size and tiles to be used
        """
        self.contexts = contexts
        return self

    def with_rooms(self, rooms):
        """
        Add rooms to configuration

        :param rooms: rooms to use
        :type rooms: [RoomGenerator]
        """
        self.room_generators = rooms
        return self

    def with_partitioners(self, partitioners):
        """
        Add partitioners to configuration

        :param partitioners: partitioners to use
        :type partitioners: [LevelPartitioner]
        """
        self.level_partitioners = partitioners
        return self

    def with_decorators(self, decorators):
        """
        Add decorators to configuration

        :param decorators: decorators to use
        :type decorators: [LevelDecorator]
        """
        self.decorators = decorators
        return self

    def with_items(self, items):
        """
        Add items to configuration

        :param items: items to use
        :type items: [ItemAdder]
        """
        self.item_adders = items
        return self

    def with_creatures(self, creatures):
        """
        Add creatures to configuration

        :param creatures: creatures to use
        :type creatures: [CreatureAdder]
        """
        self.creature_adders = creatures
        return self

    def with_portals(self, portals):
        """
        Add portals to configuration

        :param portals: portals to use
        :type portals: [PortalAdder]
        """
        self.portal_adder_configurations = portals
        return self

    def build(self):
        """
        Build configuration

        :returns: configuration for level generator factory
        :rtype: LevelGeneratorFactoryConfig
        """
        return LevelGeneratorFactoryConfig(
            model=self.model,
            room_generators=self.room_generators,
            level_partitioners=self.level_partitioners,
            decorators=self.decorators,
            item_adders=self.item_adders,
            creature_adders=self.creature_adders,
            portal_adder_configurations=self.portal_adder_configurations,
            contexts=self.contexts)


class LevelContext():
    """
    Context for level generation
    """
    def __init__(self, size, floor_type, wall_type, level_types):
        """
        Default constructor

        :param size: size of the level
        :type size: (int, int)
        :param floor_type: initial floor type to use
        :type floor_type: int
        :param wall_type: initial wall type to use
        :type wall_type: int
        """
        self.size = size
        self.floor_type = floor_type
        self.wall_type = wall_type
        self.level_types = level_types

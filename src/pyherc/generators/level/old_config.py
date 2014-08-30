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

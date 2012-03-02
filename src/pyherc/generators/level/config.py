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
Classes for configuring level generation
"""
class LevelGeneratorFactoryConfig(object):
    """
    Class to configure level generator
    """
    def __init__(self, room_generators, level_partitioners,
                 decorators, item_adders, creature_adders,
                 portal_adders, size):
        """
        Default constructor
        """
        self.__room_generators = room_generators
        self.__level_partitioners = level_partitioners
        self.__decorators = decorators
        self.__size = size
        self.item_adders = item_adders
        self.creature_adders = creature_adders
        self.__portal_adders = portal_adders

    def __get_level_partitioners(self):
        """
        Get level partitioners in this configurations
        """
        return self.__level_partitioners

    def __get_room_generators(self):
        """
        Get room generators in this configuration
        """
        return self.__room_generators

    def __get_decorators(self):
        """
        Get level decorators in this configuration
        """
        return self.__decorators

    def __get_size(self):
        """
        Get size of levels
        """
        return self.__size

    def __get_portal_adders(self):
        """
        Get portal adders
        """
        return self.__portal_adders

    level_partitioners = property(__get_level_partitioners)
    room_generators = property(__get_room_generators)
    decorators = property(__get_decorators)
    size = property(__get_size)
    portal_adders = property(__get_portal_adders)

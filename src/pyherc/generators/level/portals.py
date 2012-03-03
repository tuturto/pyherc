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
Module for adding portals
"""

from pyherc.data.dungeon import Portal

class PortalAdderConfiguration(object):
    """
    Configuration class for adding portals
    """
    def __init__(self, level_type, location_type, chance, new_level, unique):
        """
        Default constructor

        Args:
            level_type: type of level this portal can be added
            location_type: type of location to add portal
            chance: chance of portal being added 1 - 100
            new_level: name of new level
            unique: is more than one instance allowed
        """
        self.__level_type = level_type
        self.__location_type = location_type
        self.__chance = chance
        self.__new_level = new_level
        self.__unique = unique

    def __get_level_type(self):
        """
        Type of level this portal can be added
        """
        return self.__level_type

    def __get_location_type(self):
        """
        Type of location to add portal
        """
        return self.__location_type

    def __get_chance(self):
        """
        Chance of portal being added
        """
        return self.__chance

    def __get_new_level(self):
        """
        Name of the new level
        """
        return self.__new_level

    def __is_unique(self):
        """
        Is more than one instance allowed
        """
        return self.__unique

    level_type = property(__get_level_type)
    location_type = property(__get_location_type)
    chance = property(__get_chance)
    new_level = property(__get_new_level)
    is_unique = property(__is_unique)

class PortalAdderFactory(object):
    """
    Class for creating portal adders
    """
    def __init__(self, config, rng):
        """
        Default constructor

        Args:
            config: List of PortalAdderConfigurations
            rng: Random number generator
        """
        super(PortalAdderFactory, self).__init__()
        self.config = config
        self.rng = rng

    def create_portal_adders(self, level_type):
        """
        Create portal adders for level type

        Args:
            level_type: type of level to create portal adders for

        Returns:
            list of generated portal adders
        """
        adders = []
        matches = [x for x in self.config
                   if x.level_type == level_type]

        for spec in matches:
            new_adder = PortalAdder(spec.location_type,
                                    self.rng)
            adders.append(new_adder)

        return adders

class PortalAdder(object):
    """
    Basic class for adding portals
    """
    def __init__(self, location_type, rng):
        """
        Default constructor

        Args:
            location_type: type of location to add portal
            rng: Randon number generator
        """
        super(PortalAdder, self).__init__()
        self.location_type = location_type
        self.rng = rng

    def add_stairs(self, level):
        """
        Add given stairs to the level

        Args:
            level: level to modify
        """
        locations = level.get_locations_by_type(self.location_type)
        location = self.rng.choice(locations)

        portal = Portal()

        level.add_portal(portal, location)

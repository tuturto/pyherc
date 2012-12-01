#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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

from pyherc.data import Portal
from pyherc.aspects import logged

class PortalAdderConfiguration(object):
    """
    Configuration class for adding portals
    """
    @logged
    def __init__(self, icons, level_type, location_type, chance,
                 new_level, unique):
        """
        Default constructor

        :param icons: pair of icons to use for poratl and other end
        :param level_type: type of level this portal can be added
        :param location_type: type of location to add portal
        :param chance: chance of portal being added 1 - 100
        :param new_level: name of new level
        :param unique: is more than one instance allowed
        """
        self.__icons = icons
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

    def __get_icons(self):
        """
        Get pair of icons to use for portal and the other end
        """
        return self.__icons

    level_type = property(__get_level_type)
    location_type = property(__get_location_type)
    chance = property(__get_chance)
    new_level = property(__get_new_level)
    is_unique = property(__is_unique)
    icons = property(__get_icons)

class PortalAdderFactory(object):
    """
    Class for creating portal adders
    """
    @logged
    def __init__(self, config, rng):
        """
        Default constructor

        :param config: configuration to use
        :type config: [PortalAdderConfiguration]
        :param rng: random number generator
        :type rng: Random
        """
        super(PortalAdderFactory, self).__init__()
        self.config = config
        self.level_generator_factory = None
        self.rng = rng

    @logged
    def create_portal_adders(self, level_type):
        """
        Create portal adders for level type

        :param level_type: type of level to create portal adders for
        :type level_type: [string]
        :returns: generated portal adders
        :rtype: [PortalAdder]
        """
        adders = []
        matches = [x for x in self.config
                   if x.level_type == level_type]

        for spec in matches:
            new_adder = PortalAdder(spec.icons,
                                    spec.location_type,
                                    spec.new_level,
                                    self.rng)
            if spec.is_unique:
                self.config.remove(spec)
            adders.append(new_adder)

        return adders

class PortalAdder(object):
    """
    Basic class for adding portals
    """
    @logged
    def __init__(self, icons,  location_type, level_generator_name, rng):
        """
        Default constructor

        :param icons: pair of icons to use this portal and other end
        :param location_type: type of location to add portal
        :param level_generator_name: name of level generator
        :param rng: Randon number generator
        """
        super(PortalAdder, self).__init__()
        self.location_type = location_type
        self.level_generator_name = level_generator_name
        self.rng = rng
        self.icons = icons

    @logged
    def add_portal(self, level):
        """
        Add given stairs to the level

        :param level: level to modify
        :type level: Level
        """
        locations = level.get_locations_by_type(self.location_type)

        if len(locations) > 0:
            location = self.rng.choice(locations)
            portal = Portal(icons = self.icons,
                            level_generator_name = self.level_generator_name)
            level.add_portal(portal, location)

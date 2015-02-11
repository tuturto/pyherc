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
Module for adding portals
"""

from pyherc.aspects import log_debug, log_info
from pyherc.data import Portal, add_portal, get_locations_by_tag


class PortalAdderConfiguration():
    """
    Configuration class for adding portals
    """
    @log_debug
    def __init__(self, icons, level_type, location_type, chance,
                 new_level, unique, escape_stairs=False):
        """
        Default constructor

        :param icons: pair of icons to use for poratl and other end
        :param level_type: type of level this portal can be added
        :param location_type: type of location to add portal
        :param chance: chance of portal being added 1 - 100
        :param new_level: name of new level
        :param unique: is more than one instance allowed
        :param escape_stairs: are there stairs leading out of the dungeon
        """
        self.icons = icons
        self.level_type = level_type
        self.location_type = location_type
        self.chance = chance
        self.new_level = new_level
        self.is_unique = unique
        self.is_escape_stairs = escape_stairs


class PortalAdderFactory():
    """
    Class for creating portal adders
    """
    @log_debug
    def __init__(self, config, rng):
        """
        Default constructor

        :param config: configuration to use
        :type config: [PortalAdderConfiguration]
        :param rng: random number generator
        :type rng: Random
        """
        super().__init__()
        self.config = config
        self.level_generator_factory = None
        self.rng = rng

    @log_info
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
                   if x.level_type == level_type
                   and self.rng.randint(0, 100) <= x.chance]

        for spec in matches:
            new_adder = PortalAdder(spec.icons,
                                    spec.location_type,
                                    spec.new_level,
                                    spec.is_escape_stairs,
                                    self.rng)
            if spec.is_unique:
                self.config.remove(spec)
            adders.append(new_adder)

        return adders


class PortalAdder():
    """
    Basic class for adding portals
    """
    @log_debug
    def __init__(self, icons,  location_type, level_generator_name,
                 escape_stairs, rng):
        """
        Default constructor

        :param icons: pair of icons to use this portal and other end
        :param location_type: type of location to add portal
        :param level_generator_name: name of level generator
        :param rng: Randon number generator
        """
        super().__init__()
        self.location_type = location_type
        self.level_generator_name = level_generator_name
        self.rng = rng
        self.icons = icons
        self.escape_stairs = escape_stairs

    @log_info
    def add_portal(self, level):
        """
        Add given stairs to the level

        :param level: level to modify
        :type level: Level
        """
        locations = list(get_locations_by_tag(level, self.location_type))

        if len(locations) > 0:
            location = self.rng.choice(locations)
            portal = Portal(icons=self.icons,
                            level_generator_name=self.level_generator_name)
            portal.exits_dungeon = self.escape_stairs
            add_portal(level, location, portal)

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
Module for adding portals
"""

from pyherc.aspects import log_debug, log_info
from pyherc.data import (Portal, add_portal, get_locations_by_tag,
                         blocks_movement, safe_passage)


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

    def __call__(self, level):
        """
        Add given stairs to the level
        """
        self.add_portal(level)

    @log_info
    def add_portal(self, level):
        """
        Add given stairs to the level

        :param level: level to modify
        :type level: Level
        """
        locations = [x for x in get_locations_by_tag(level, self.location_type)
                     if safe_passage(level, x)]

        if locations:
            location = self.rng.choice(locations)
            portal = Portal(icons=self.icons,
                            level_generator_name=self.level_generator_name)
            portal.exits_dungeon = self.escape_stairs
            add_portal(level, location, portal)

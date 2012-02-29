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
Module for adding stairs
"""

class PortalAdder(object):
    """
    Basic class for adding stairs
    """
    def __init__(self, rng):
        """
        Default constructor

        Args:
            rng: Randon number generator
        """
        super(PortalAdder, self).__init__()
        self.rng = rng

    def add_stairs(self, level, stairs):
        """
        Add given stairs to the level

        Args:
            level: level to modify
            stairs: stairs to add
        """
        rooms = level.get_locations_by_type('room')
        location = self.rng.choice(rooms)
        level.add_portal(stairs, location)

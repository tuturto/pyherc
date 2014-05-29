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
Module for customer matchers used in testing
"""

from hamcrest.core.base_matcher import BaseMatcher
from pyherc.data import wall_tile, get_tile, get_tiles, get_location_tags
from pyherc.data import floor_tile

class MapConnectivity(BaseMatcher):
    """
    Helper class used to verify if generated level is fully connected
    """
    def __init__(self):
        """
        Initialise this matcher
        """
        super().__init__()

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        all_points = self.get_all_points(item, None)

        if len(all_points) > 0:
            connected_points = self.get_connected_points(item,
                                                         all_points[0],
                                                         None,
                                                         [])
            connected = True
            for point in all_points:
                if not point in connected_points:
                    connected = False
        else:
            connected = False

        return connected

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append('Level')

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Unconnected level')

    def get_all_points(self, level, open_tile):
        """
        Get all open points in level

        Args:
            open: ID of tile considered open

        Returns:
            List of all open points in level
        """
        points = []

        for location, tile in get_tiles(level):
            if tile['\ufdd0:wall'] == None:
                points.append(location)

        return points

    def get_connected_points(self, level, start, open_tile, connected_points):
        """
        Get all points that are connected to a given point

        Args:
            level: level to check
            start: start location
            open: ID of tile considered open

        Returns:
            list of connected points
        """
        x_loc = start[0]
        y_loc = start[1]

        if start in connected_points:
            return None

        if get_tile(level, start) is None:
            return None

        if wall_tile(level, start) is None and floor_tile(level, start) is not None:
            connected_points.append(start)
            self.get_connected_points(level, (x_loc, y_loc - 1),
                                      open_tile,
                                      connected_points)
            self.get_connected_points(level, (x_loc, y_loc + 1),
                                      open_tile,
                                      connected_points)
            self.get_connected_points(level, (x_loc - 1, y_loc),
                                      open_tile,
                                      connected_points)
            self.get_connected_points(level, (x_loc + 1, y_loc),
                                      open_tile,
                                      connected_points)

            self.get_connected_points(level, (x_loc - 1, y_loc - 1),
                                      open_tile,
                                      connected_points)
            self.get_connected_points(level, (x_loc - 1, y_loc + 1),
                                      open_tile,
                                      connected_points)
            self.get_connected_points(level, (x_loc - 1, y_loc - 1),
                                      open_tile,
                                      connected_points)
            self.get_connected_points(level, (x_loc + 1, y_loc + 1),
                                      open_tile,
                                      connected_points)

        return connected_points


def is_fully_accessible():
    """
    Check if level is fully connected

    :param open_tile: tile_id to use for empty walls
    :type open_tile: int
    """
    return MapConnectivity()


def located_in_room(entity):
    """
    Check if given entity is located in room

    :param entity: entity to check
    :returns: True if located in room, False otherwise
    :rtype: Boolean
    """
    level = entity.level

    if 'room' in get_location_tags(level, entity.location):
        return True
    else:
        return False

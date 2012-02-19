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
Module for customer matchers used in testing
"""

class MapConnectivity():
    """
    Helper class used to verify if generated level is fully connected
    """
    def __init__(self, level):
        """
        Initialise this matcher

        Args:
            level: Level to check for connectivity
        """
        self.level = level
        self.all_points = []
        self.connected_points = []
        self.connected = None

    def is_connected(self, open):
        """
        Checks if given level is fully connected

        Args:
            open: ID of tile considered open

        Returns:
            True if level is connected, otherwise False
        """
        self.all_points = self.get_all_points(open)

        if len(self.all_points) > 0:
            self.get_connected_points(self.all_points[0], open)
            self.connected = True
            for point in self.all_points:
                if not point in self.connected_points:
                    self.connected = False
        else:
            self.connected = False

        return self.connected

    def get_all_points(self, open):
        """
        Get all open points in level

        Args:
            open: ID of tile considered open

        Returns:
            List of all open points in level
        """
        points = []

        for loc_y in range(len(self.level.walls[0])):
            for loc_x in range(len(self.level.walls)):
                if self.level.walls[loc_x][loc_y] == open:
                    points.append((loc_x, loc_y))

        return points

    def get_connected_points(self, start, open):
        """
        Get all points that are connected to a given point

        Args:
            start: start location
            open: ID of tile considered open
        """
        x_loc = start[0]
        y_loc = start[1]

        if start in self.connected_points:
            return None

        if x_loc < 0 or x_loc > len(self.level.walls):
            return None

        if y_loc < 0 or y_loc > len(self.level.walls[0]):
            return None

        if self.level.walls[x_loc][y_loc] == open:
            self.connected_points.append(start)
            self.get_connected_points((x_loc, y_loc - 1), open)
            self.get_connected_points((x_loc, y_loc + 1), open)
            self.get_connected_points((x_loc - 1, y_loc), open)
            self.get_connected_points((x_loc + 1, y_loc), open)

def map_accessibility_in(level, open):
    """
    Check that the map is fully connected

    Args:
        level: Level to check
        open: ID of tile considered open

    Returns:
        True if level is fully connected, False otherwise
    """
    connectivity = MapConnectivity(level)
    return connectivity.is_connected(open)

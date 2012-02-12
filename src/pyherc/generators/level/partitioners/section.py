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
Classes to represent division of levels
"""

class Section(object):
    """
    Class representing a single section in a level
    """
    def __init__(self, corner1, corner2):
        """
        Default constructor

        Args:
            corner1: Coordinates of first corner
            corner2: Coordinates of the second corner
        """
        self.__corners = []
        self.__corners.append(corner1)
        self.__corners.append(corner2)

        self.__connections = []
        self.__neighbours = []

        self.connection_points = []

    def __get_corners(self):
        """
        Get corners of this section
        """
        return self.__corners

    def __set_corners(self, corners):
        """
        Set corners of this section
        @param corners: corners to set
        """
        self.__corners = corners

    def __get_connections(self):
        """
        List of connections this section has
        """
        return self.__connections

    def __get_neighbours(self):
        """
        List of sections next to this one
        """
        return self.__neighbours

    def __get_connected(self):
        """
        Is this section connected to a neighbour

        Returns:
            True if connected, otherwise False
        """
        return len(self.__connections) > 0

    def __get_left_edge(self):
        """
        Get leftmost point of the section

        Returns:
            Leftmost point of the section
        """
        point1 = self.__corners[0][0]
        point2 = self.__corners[1][0]

        if point1 < point2:
            return point1
        else:
            return point2

    def __get_width(self):
        """
        Get width of the section

        Returns:
            Width of the section
        """
        return abs(self.__corners[0][0] - self.__corners[1][0])

    def __get_top_edge(self):
        """
        Get top edge of the section

        Returns:
            Highest point of the section
        """
        point1 = self.__corners[0][1]
        point2 = self.__corners[1][1]

        if point1 < point2:
            return point1
        else:
            return point2

    def __get_height(self):
        """
        Get height of the section

        Returns:
            Height of the section
        """
        return abs(self.__corners[0][1] - self.__corners[1][1])

    corners = property(__get_corners, __set_corners)
    """Corners of this Section.""" #pylint: disable=W0105

    connections = property(__get_connections)
    """Readonly property to access connections of the section""" #pylint: disable=W0105

    neighbours = property(__get_neighbours)
    """Readonly property to access neighbours of the section""" #pylint: disable=W0105

    connected = property(__get_connected)
    """Readonly property for connection status of the section

        Returns:
            True if section is connected, otherwise False""" #pylint: disable=W0105

    left_edge = property(__get_left_edge)
    """Readonly property to find leftmost point of the section""" #pylint: disable=W0105

    width = property(__get_width)
    """Readonly property to calculate width of the section""" #pylint: disable=W0105

    top_edge = property(__get_top_edge)
    """Readonly property to find topmost point of the section""" #pylint: disable=W0105

    height = property(__get_height)
    """Readonly property to find height of the section""" #pylint: disable=W0105

    def connect_to(self, section):
        '''
        Connect this Section to another

        Args:
            section: Section to connect to
        '''
        self.connections.append(section)
        section.connections.append(self)

    def unconnected_neighbours(self):
        '''
        Get list of unconnected neighbours

        Returns:
            List of unconnected neighbours
        '''
        return [x for x in self.neighbours
                        if x.connected == False]

    def has_unconnected_neighbours(self):
        '''
        Check if any of this Sections neighbours is unconnected

        Returns:
            True if unconnected neighbour is found, otherwise false
        '''
        return len(self.unconnected_neighbours()) > 0

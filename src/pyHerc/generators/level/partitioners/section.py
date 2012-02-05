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

class Section(object):
    '''
    Class representing a single section in a level
    '''
    def __init__(self, corners):
        '''
        Default constructor
        '''
        self.__corners = corners
        self.__connected = False
        self.__connections = []
        self.__neighbours = []

    def get_corners(self):
        '''
        Get corners of this section
        '''
        return self.__corners

    def set_corners(self, corners):
        '''
        Set corners of this section
        @param corners: corners to set
        '''
        self.__corners = corners

    def get_connections(self):
        '''
        List of connections this section has
        '''
        return self.__connections

    def get_neighbours(self):
        '''
        List of sections next to this one
        '''
        return self.__neighbours

    def get_connected(self):
        '''
        Is this section connected to a neighbour
        '''
        return self.__connected

    def set_connected(self, value):
        self.__connected = value

    corners = property(get_corners)
    connections = property(get_connections)
    neighbours = property(get_neighbours)
    connected = property(get_connected, set_connected)

    def connect_to(self, section):
        '''
        Connect this Section to another
        '''
        self.connected = True
        section.connected = True
        self.connections.append(section)
        section.connections.append(self)

    def unconnected_neighbours(self):
        '''
        Get list of unconnected neighbours
        @returns: List of unconnected neighbours
        '''
        return [x for x in self.neighbours
                        if x.connected == False]

    def has_unconnected_neighbours(self):
        '''
        Check if any of this Sections neighbours is unconnected
        @returns: True if unconnected neighbour is found, otherwise false
        '''
        return len(self.unconnected_neighbours()) > 0

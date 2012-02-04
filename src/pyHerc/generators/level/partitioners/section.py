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

    @property
    def corners(self):
        '''
        Get corners of this section
        '''
        return self.__corners

    @corners.setter
    def corners(self, value):
        '''
        Set corners of this section
        '''
        self.__corners = value

    @property
    def connections(self):
        '''
        List of connections this section has
        '''
        return self.__connections

    @property
    def neighbours(self):
        '''
        List of sections next to this one
        '''
        return self.__neighbours

    @property
    def connected(self):
        '''
        Is this section connected to a neighbour
        '''
        return self.__connected

    @connected.setter
    def connected(self, value):
        self.__connected = value

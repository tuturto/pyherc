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

'''
Tests for Section
'''
from pyherc.generators.level.partitioners.section import Section

class TestSectionConnections():
    '''
    Class for testing Section
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def setup(self):
        '''
        Setup test case
        '''
        self.section1 = Section(())
        self.section2 = Section(())

        self.section1.neighbours.append(self.section2)
        self.section2.neighbours.append(self.section1)

    def test_unconnected_neighbours(self):
        '''
        Test that unconnected neighbours can be detected
        '''
        assert self.section1.has_unconnected_neighbours() == True

    def test_connected_neighbours_are_not_reported(self):
        '''
        Test that connected neighbours are not reported as unconnected
        '''
        self.section1.connect_to(self.section2)

        assert self.section1.has_unconnected_neighbours() == False

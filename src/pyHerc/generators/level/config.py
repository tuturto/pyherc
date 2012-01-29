#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

'''
Classes for configuring level generation
'''
class LevelGeneratorConfig():
    '''
    Class to configure level generator
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        self.room_generators = []
        self.__level_partitioners = []
        self.decorators = []

    def get_level_partitioners(self):
        '''
        Get level partitioners in this configurations
        '''
        return self.level_partitioners

    level_partitioners = property(get_level_partitioners)




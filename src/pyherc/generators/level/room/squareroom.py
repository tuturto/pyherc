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
Classes for generating square rooms
'''

import logging

class SquareRoom(object):
    '''
    Class for generating a square room
    '''
    def __init__(self, floor_tile, empty_tile):
        '''
        Default constructor

        Args:
            floor_tile: id of the tile to use for floors
            empty_tile: id of the empty wall tile
        '''
        self.floor_tile = floor_tile
        self.empty_tile = empty_tile
        self.logger = logging.getLogger('pyherc.generators.level.room.squareroom.SquareRoom') #pylint disable:W0301

    def generate_room(self, level, section):
        '''
        Generate room

        Args:
            level: Level to modify
            section: Section that generator is allowed to change
        '''
        self.logger.debug('generating room for area {0}'.format(
                                                            section.corners))
        section_left_edge = section.corners[0][0]
        section_right_edge = section.corners[1][0]
        section_top_edge = section.corners[0][1]
        section_bottom_edge = section.corners[1][1]

        section_width = abs(section_right_edge - section_left_edge)
        section_height = abs(section_bottom_edge - section_top_edge)

        room_width = int(section_width * 0.75)
        room_height = int(section_height * 0.75)

        room_left_edge = section_left_edge + (
                                    (section_width - room_width) // 2)
        room_right_edge = room_left_edge + room_width
        room_top_edge = section_top_edge + (
                                    (section_height - room_height) // 2)
        room_bottom_edge = room_top_edge + room_height

        for loc_y in range(room_top_edge, room_bottom_edge):
            for loc_x in range(room_left_edge, room_right_edge):
                level.floor[loc_x][loc_y] = self.floor_tile
                level.walls[loc_x][loc_y] =self.empty_tile

        self.logger.debug('room generated')

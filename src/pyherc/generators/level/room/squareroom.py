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

class SquareRoomGenerator(object):
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
        self.room_width = None
        self.room_height = None
        self.logger = logging.getLogger('pyherc.generators.level.room.squareroom.SquareRoomGenerator') #pylint disable=C0301

    def generate_room(self, level, section):
        '''
        Generate room

        Args:
            level: Level to modify
            section: Section that generator is allowed to change
        '''
        self.logger.debug('generating room for area {0}'.format(
                                                            section.corners))

        self.room_width = int(section.width * 0.50)
        self.room_height = int(section.height * 0.50)

        room_left_edge = section.left_edge + (
                                    (section.width - self.room_width) // 2)
        room_right_edge = room_left_edge + self.room_width
        room_top_edge = section.top_edge + (
                                    (section.height - self.room_height) // 2)
        room_bottom_edge = room_top_edge + self.room_height

        for loc_y in range(room_top_edge, room_bottom_edge):
            for loc_x in range(room_left_edge, room_right_edge):
                level.floor[loc_x][loc_y] = self.floor_tile
                level.walls[loc_x][loc_y] = self.empty_tile

        self.logger.debug(level.dump_string())

        section.add_room_connection(None, None)
        section.add_room_connection(None, None)
        section.add_room_connection(None, None)
        section.add_room_connection(None, None)

        self.logger.debug('room generated')


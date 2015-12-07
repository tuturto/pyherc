# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Classes for generating catacombs
"""
from pyherc.aspects import log_debug
from pyherc.generators.utils import BSPSection
from pyherc.generators.level.partitioners import (section_width, section_height,
                                                  section_floor, section_wall)

class CatacombsGenerator():
    """
    Class for generating a catacomblike rooms
    """
    @log_debug
    def __init__(self, floor_tile, empty_tile, level_types, rng):
        """
        Default constructor

        :param floor_tile: id of the tile to use for floors
        :type floor_tile: integer
        :param empty_tile: id of the empty wall tile
        :type empty_tile: integer
        :param level_types: types of level this generator can be used
        :type level_types: [string]
        :param rng: random number generator
        :type rng: Random
        """
        self.floor_tile = floor_tile
        self.empty_tile = empty_tile
        self.room_width = None
        self.room_height = None
        self.level_types = level_types
        self.rng = rng

    def __call__(self, section):
        """
        Generate room
        """
        self.generate_room(section)

    @log_debug
    def generate_room(self, section):
        """
        Generate room

        :param section: section for generator to draw to
        :type section: Section
        """
        level_size = (section_width(section), section_height(section))
        room_min_size = (3, 3)
        BSPStack = []
        BSP = BSPSection((0, 0),
                         (level_size[0] - 2,
                          level_size[1] - 2),
                         None)
        BSPStack.append(BSP)
        room_stack = []

        while len(BSPStack) > 0:
            tempBSP = BSPStack.pop()
            tempBSP.split(min_size=(room_min_size[0] + 4,
                                    room_min_size[1] + 4))
            if tempBSP.node1 is not None:
                BSPStack.append(tempBSP.node1)
            if tempBSP.node2 is not None:
                BSPStack.append(tempBSP.node2)
            if tempBSP.node1 is None and tempBSP.node2 is None:
                #leaf
                room_stack.append(tempBSP)

        for room in room_stack:
            corner1 = (room.corner1[0] + self.rng.randint(1, 4),
                       room.corner1[1] + self.rng.randint(1, 4))
            corner2 = (room.corner2[0] - self.rng.randint(1, 4),
                       room.corner2[1] - self.rng.randint(1, 4))

            for y in range(corner1[1], corner2[1] + 1):
                for x in range(corner1[0], corner2[0] + 1):
                    section_floor(section, 
                                  (x, y),
                                  self.floor_tile,
                                  'room')
                    section_wall(section,
                                 (x, y),
                                 self.empty_tile,
                                 None)

        area_queue = BSP.get_area_queue()
        area_queue.reverse()

        while len(area_queue) > 1:
            area1 = area_queue.pop()
            area2 = area_queue.pop()
            center1 = area1.get_center()
            center2 = area2.get_center()
            #connect these two areas
            if area1.direction == 1:
                #areas on top of each other
                if center1[1] < center2[1]:
                    for y in range(center1[1], center2[1] + 1):
                        section_floor(section,
                                      (center1[0], y),
                                      self.floor_tile,
                                      'corridor')
                        section_wall(section,
                                     (center1[0], y),
                                     self.empty_tile,
                                     None)
                else:
                    for y in range(center2[1], center1[1] + 1):
                        section_floor(section, 
                                      (center1[0], y),
                                      self.floor_tile,
                                      'corridor')
                        section_wall(section,
                                     (center1[0], y),
                                     self.empty_tile,
                                     None)
            else:
                #areas next to each other
                if center1[0] < center2[0]:
                    for x in range(center1[0], center2[0] + 1):
                        section_floor(section,
                                      (x, center1[1]),
                                      self.floor_tile,
                                      'corridor')
                        section_wall(section,
                                     (x, center1[1]),
                                     self.empty_tile,
                                     None)
                else:
                    for x in range(center2[0], center1[0] + 1):
                        section_floor(section,
                                      (x, center1[1]),
                                      self.floor_tile,
                                      'corridor')
                        section_wall(section,
                                     (x, center1[1]),
                                     self.empty_tile,
                                     None)

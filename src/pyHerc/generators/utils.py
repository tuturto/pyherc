#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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

import random
import logging
import collections

class BSPSection:
    """
    Class used to divide area in sections
    """
    def __init__(self):
        self.corner1 = None
        self.corner2 = None
        self.node1 = None
        self.node2 = None
        self.parent = None
        self.direction = None
        self.logger = logging.getLogger('pyHerc.generators.utils.BSPSection')

    def __init__(self, corner1, corner2, parent, direction = None):
        self.corner1 = corner1
        self.corner2 = corner2
        self.node1 = None
        self.node2 = None
        self.parent = parent
        self.direction = direction
        self.logger = logging.getLogger('pyHerc.generators.utils.BSPSection')
        self.logger.debug('created new BSP section with corners ' +
                                    self.corner1.__str__() + ' and ' + self.corner2.__str__())

    def split(self, minSize = (6, 6), direction = None):
        """
        Split BSPSection in two
        Links two new BSPSections into this one
        @param minSize: minimum size to split into
        @param direction: horizontal (1) / vertical split (2)
        """
        assert(self.corner1 != None)
        assert(self.corner2 != None)

        size = (abs(self.corner1[0] - self.corner2[0]),
                    abs(self.corner1[1] - self.corner2[1]))
        self.logger.debug('splitting BSP section of size ' + size.__str__())

        if direction == None:
            direction = random.randint(1, 2) # 1 split horisontal, 2 split vertical
        assert(direction in (1, 2))

        if direction == 1:
            if size[1] < 2 * minSize[1]:
                if size[0] < 2 * minSize[0]:
                    return None
                else:
                    direction = 2
        else:
            if size[0] < 2 * minSize[0]:
                if size[1] < 2 * minSize[1]:
                    return None
                else:
                    direction = 1

        if direction == 1:
            self.logger.debug('split direction horizontal')
            splitLocation = random.randint(minSize[1], size[1] - minSize[1])
            self.logger.debug('split location ' + splitLocation.__str__())
            self.node1 = BSPSection(self.corner1, (self.corner2[0], self.corner1[1] + splitLocation),
                                                self, direction)
            self.node2 = BSPSection((self.corner1[0], self.corner1[1] + splitLocation + 1),  self.corner2,
                                                self, direction)
        else:
            self.logger.debug('split direction vertical')
            splitLocation = random.randint(minSize[0], size[0] - minSize[0])
            self.logger.debug('split location ' + splitLocation.__str__())
            self.node1 = BSPSection(self.corner1, (self.corner1[0] + splitLocation, self.corner2[1]),
                                                self, direction)
            self.node2 = BSPSection((self.corner1[0] + splitLocation + 1, self.corner1[1]), self.corner2,
                                                self, direction)

        self.logger.debug('split performed')

    def __str__(self):
        str = ''
        if self.corner1 != None:
            if self.corner2 != None:
                return self.corner1.__str__() + ':' + self.corner2.__str__()
            else:
                return self.corner1.__str__() + ':None'
        else:
            if self.corner2 != None:
                return 'None:' + self.corner2.__str__()
            else:
                return 'None:None'

    def getAreaQueue(self):
        """
        Gets list of BSPSections, starting from leaves and progressing towards root
        """
        queue = collections.deque()
        list = []
        queue.append(self)

        while len(queue) > 0:
            item = queue.pop()
            list.append(item)
            if item.node1 != None:
                queue.appendleft(item.node1)
            if item.node2 != None:
                queue.appendleft(item.node2)

        list.reverse()

        return list

    def getCenter(self):
        """
        Calculates center of the BSPSection
        @return: center point
        """
        assert(self.corner1 != None)
        assert(self.corner2 != None)
        center = (int(self.corner1[0] + ((self.corner2[0] - self.corner1[0]) / 2)),
                        int(self.corner1[1] + ((self.corner2[1] - self.corner1[1]) / 2)))

        return center
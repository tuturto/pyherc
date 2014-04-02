# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
Utility classes

BSPSection
"""

import collections
import logging
import random


class BSPSection():
    """
    Class used to divide area in sections
    """
    def __init__(self, corner1=None, corner2=None, parent=None,
                 direction=None):
        """
        Default constructor
        """
        self.corner1 = corner1
        self.corner2 = corner2
        self.node1 = None
        self.node2 = None
        self.parent = parent
        self.direction = direction
        self.logger = logging.getLogger('pyherc.generators.utils.BSPSection')

    def split(self, min_size=(6, 6), direction=None):
        """
        Split BSPSection in two
        Links two new BSPSections into this one
        :param min_size: minimum size to split into
        :param direction: horizontal (1) / vertical split (2)
        """
        assert self.corner1 is not None
        assert self.corner2 is not None

        size = (abs(self.corner1[0] - self.corner2[0]),
                abs(self.corner1[1] - self.corner2[1]))

        if direction is None:
            # 1 split horizontal, 2 split vertical
            direction = random.randint(1, 2)
        assert(direction in (1, 2))

        if direction == 1:
            if size[1] < 2 * min_size[1]:
                if size[0] < 2 * min_size[0]:
                    return None
                else:
                    direction = 2
        else:
            if size[0] < 2 * min_size[0]:
                if size[1] < 2 * min_size[1]:
                    return None
                else:
                    direction = 1

        if direction == 1:
            split_location = random.randint(min_size[1], size[1] - min_size[1])
            self.node1 = BSPSection(self.corner1,
                                    (self.corner2[0],
                                        self.corner1[1] + split_location),
                                    self, direction)
            self.node2 = BSPSection((self.corner1[0],
                                     self.corner1[1] + split_location + 1),
                                    self.corner2,
                                    self, direction)
        else:
            split_location = random.randint(min_size[0], size[0] - min_size[0])
            self.node1 = BSPSection(self.corner1,
                                    (self.corner1[0] + split_location,
                                     self.corner2[1]),
                                    self, direction)
            self.node2 = BSPSection((self.corner1[0] + split_location + 1,
                                    self.corner1[1]),
                                    self.corner2,
                                    self, direction)

    def __str__(self):
        """
        Override __str__ to print meaningful string representation
        """
        if self.corner1 is not None:
            if self.corner2 is not None:
                return self.corner1.__str__() + ':' + self.corner2.__str__()
            else:
                return self.corner1.__str__() + ':None'
        else:
            if self.corner2 is not None:
                return 'None:' + self.corner2.__str__()
            else:
                return 'None:None'

    def get_area_queue(self):
        """
        Gets list of BSPSections, starting from leaves and moving towards root
        """
        queue = collections.deque()
        list = []
        queue.append(self)

        while len(queue) > 0:
            item = queue.pop()
            list.append(item)
            if item.node1 is not None:
                queue.appendleft(item.node1)
            if item.node2 is not None:
                queue.appendleft(item.node2)

        list.reverse()

        return list

    def get_center(self):
        """
        Calculates center of the BSPSection
        :returns: center point
        """
        assert self.corner1 is not None
        assert self.corner2 is not None
        center = (int(self.corner1[0] +
                  ((self.corner2[0] - self.corner1[0]) / 2)),
                  int(self.corner1[1] +
                      ((self.corner2[1] - self.corner1[1]) / 2)))

        return center

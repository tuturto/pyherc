# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
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
Module for handling loading of images and icons
"""

import herculeum.ui.gui.resources
from pyherc.aspects import log_debug
from PyQt4.QtCore import QRect
from PyQt4.QtGui import QPixmap


class QtSurfaceManager():
    """
    Class for managing images and icons
    """
    @log_debug
    def __init__(self):
        """
        Default constructor
        """
        super(QtSurfaceManager, self).__init__()
        self.icons = {}
        self.images = {}
        self.tilesets = None
        self.resourcesLoaded = 0

    @log_debug
    def __load_image(self, image_name):
        """
        Load a file and return corresponding surface object

        :param image_name: file name
        :type image_name: string

        :returns: image
        :rtype: QPixmap
        """
        image = QPixmap()
        image.load(image_name)

        return image

    @log_debug
    def add_icon(self, key, filename, ascii_char, attributes = None):
        """
        Add icon to internal collection
        """
        if not key in self.icons:
            surface = self.__load_image(filename)
            self.icons[key] = surface

        return key

    @log_debug
    def load_resources(self):
        """
        Load graphics from files

        """
        surface = self.__load_image(':transparent.png')
        self.icons['transparent'] = surface

        self.icons['heart_red_0'] = self.__load_image(':ui/heart_red_0.png')
        self.icons['heart_red_1'] = self.__load_image(':ui/heart_red_1.png')
        self.icons['heart_red_2'] = self.__load_image(':ui/heart_red_2.png')
        self.icons['heart_red_3'] = self.__load_image(':ui/heart_red_3.png')
        self.icons['heart_red_4'] = self.__load_image(':ui/heart_red_4.png')

        self.icons['heart_blue_0'] = self.__load_image(':ui/heart_blue_0.png')
        self.icons['heart_blue_1'] = self.__load_image(':ui/heart_blue_1.png')
        self.icons['heart_blue_2'] = self.__load_image(':ui/heart_blue_2.png')
        self.icons['heart_blue_3'] = self.__load_image(':ui/heart_blue_3.png')
        self.icons['heart_blue_4'] = self.__load_image(':ui/heart_blue_4.png')

        self.icons['arrow_left'] = self.__load_image(':ui/arrow_left.png')
        self.icons['arrow_right'] = self.__load_image(':ui/arrow_right.png')

    def __load_tilesets(self):
        self.tilesets = {}
        self.tilesets['floors'] = self.__load_image(':floor.png')

    def load_floor(self, offset, set_name):
        """
        Load floor set
        """
        if not self.tilesets:
            self.__load_tilesets()

        tiles = self.tilesets['floors']
        size = 32

        self.icons[set_name + "_35"] = tiles.copy(QRect(offset[0] * size,
                                                        offset[1] * size,
                                                        size,
                                                        size))
        self.icons[set_name + "_357"] = tiles.copy(QRect(offset[0] * size + size,
                                                         offset[1] * size,
                                                         size,
                                                         size))
        self.icons[set_name + "_57"] = tiles.copy(QRect(offset[0] * size + size * 2,
                                                        offset[1] * size,
                                                        size,
                                                        size))
        self.icons[set_name + "_5"] = tiles.copy(QRect(offset[0] * size + size * 3,
                                                      offset[1] * size,
                                                      size,
                                                      size))
        self.icons[set_name] = tiles.copy(QRect(offset[0] * size + size * 5,
                                                offset[1] * size,
                                                size,
                                                size))
        self.icons[set_name + "_135"] = tiles.copy(QRect(offset[0] * size,
                                                         offset[1] * size + size,
                                                         size,
                                                         size))
        self.icons[set_name + "_1357"] = tiles.copy(QRect(offset[0] * size + size,
                                                          offset[1] * size + size,
                                                          size,
                                                          size))
        self.icons[set_name + "_157"] = tiles.copy(QRect(offset[0] * size + size * 2,
                                                         offset[1] * size + size,
                                                         size,
                                                         size))
        self.icons[set_name + "_15"] = tiles.copy(QRect(offset[0] * size + size * 3,
                                                        offset[1] * size + size,
                                                        size,
                                                        size))
        self.icons[set_name + "_3"] = tiles.copy(QRect(offset[0] * size + size * 4,
                                                       offset[1] * size + size,
                                                       size,
                                                       size))
        self.icons[set_name + "_37"] = tiles.copy(QRect(offset[0] * size + size * 5,
                                                        offset[1] * size + size,
                                                        size,
                                                        size))
        self.icons[set_name + "_7"] = tiles.copy(QRect(offset[0] * size + size * 6,
                                                       offset[1] * size + size,
                                                       size,
                                                       size))
        self.icons[set_name + "_13"] = tiles.copy(QRect(offset[0] * size,
                                                        offset[1] * size + size * 2,
                                                        size,
                                                        size))
        self.icons[set_name + "_137"] = tiles.copy(QRect(offset[0] * size + size,
                                                         offset[1] * size + size * 2,
                                                         size,
                                                         size))
        self.icons[set_name + "_17"] = tiles.copy(QRect(offset[0] * size + size * 2,
                                                        offset[1] * size + size * 2,
                                                        size,
                                                        size))
        self.icons[set_name + "_1"] = tiles.copy(QRect(offset[0] * size + size * 3,
                                                       offset[1] * size + size * 2,
                                                       size,
                                                       size))
    
    @log_debug
    def split_surface(self, image, tile_size):
        """
        Split image to tiles

        :param image: image to split
        :type image: QPixmap
        :param tile_size: size of the tile
        :type tile_size: (int, int)
        :returns: array of tiles
        :rtype: [QPixmap]
        """
        tiles = []
        image_width = image.width()
        image_height = image.height()

        tile_width = tile_size[0]
        tile_height = tile_size[1]

        x_repeats = image_width / tile_width
        y_repeats = image_height / tile_height

        for loc_y in range(y_repeats):
            for loc_x in range(x_repeats):
                rect = QRect(loc_x * tile_width,
                             loc_y * tile_height,
                             tile_width,
                             tile_height)

                sub_image = image.copy(rect)
                tiles.append(sub_image)

        return tiles

    def get_image(self, id):
        """
        Get image with ID

        :param id: ID number of the image to retrieve
        :type id: int
        :returns: image
        :rtype: QPixmap
        """
        return self.images[id]

    def get_icon(self, id):
        """
        Get icon with ID

        :param id: ID number of the icon to retrieve
        :type id: int
        :returns: icon if found, otherwise empty icon
        :rtype: QPixmap
        """
        if not id:
            return self.icons['transparent']

        if not hasattr(id, 'upper'):
            tiles = []
            for sub_id in id:
                tiles.append(self.get_icon(sub_id))
            return tiles
        else:
            if id in self.icons:
                return self.icons[id]
            else:
                return self.icons['transparent']

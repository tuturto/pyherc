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
                if sub_id in self.icons:
                    tiles.append(self.icons[sub_id])
            return tiles
        else:
            if id in self.icons:
                return self.icons[id]
            else:
                return self.icons['transparent']

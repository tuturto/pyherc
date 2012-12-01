#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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

import os, os.path
import images
import herculeum.config.tiles
import pyherc

from pyherc.aspects import logged
from PyQt4.QtGui import QPixmap
from PyQt4.QtSvg import QSvgWidget
from PyQt4.QtCore import QRect

class SurfaceManager:
    """
    Class for managing images and icons
    """
    @logged
    def __init__(self, base_path):
        """
        Default constructor
        """
        self.icons = {}
        self.images = {}
        self.resourcesLoaded = 0
        self.base_path = base_path

    def __load_image(self, base_path, image_name):
        """
        Load a file and return corresponding surface object

        :param base_path: directory of the file
        :type base_path: string
        :param image_name: file name
        :type image_name: string

        :returns: image
        :rtype: QPixmap
        """
        image = QPixmap()
        image.load(os.path.join(base_path, image_name))

        return image

    @logged
    def add_icon(self, key, filename):
        """
        Add icon to internal collection
        """
        if not key in self.icons:
            surface = self.__load_image(self.base_path, filename)
            self.icons[key] = surface

        return key

    @logged
    def load_resources(self, base_path):
        """
        Load graphics from files

        :param base_path: path to directory where resources are location
        :type base_path: string
        """
        surface = self.__load_image(base_path, 'transparent.png')
        self.icons[herculeum.config.tiles.TRANSPARENT] = surface

        surface = self.__load_image(base_path, 'weapons.png')

        tiles = self.split_surface(surface, (32, 32))

        self.icons[herculeum.config.tiles.ITEM_MORNING_STAR_1] = tiles[22]
        self.icons[herculeum.config.tiles.ITEM_MORNING_STAR_2] = tiles[23]
        self.icons[herculeum.config.tiles.ITEM_SHORT_SWORD_1] = tiles[6]
        self.icons[herculeum.config.tiles.ITEM_SHORT_SWORD_2] = tiles[6]
        self.icons[herculeum.config.tiles.ITEM_LIGHT_MACE] = tiles[20]
        self.icons[herculeum.config.tiles.ITEM_SICKLE] = tiles[41]
        self.icons[herculeum.config.tiles.ITEM_CLUB] = tiles[21]
        self.icons[herculeum.config.tiles.ITEM_MACE] = tiles[24]
        self.icons[herculeum.config.tiles.ITEM_SHORTSPEAR] = tiles[28]
        self.icons[herculeum.config.tiles.ITEM_LONGSPEAR] = tiles[34]
        self.icons[herculeum.config.tiles.ITEM_SPEAR] = tiles[30]

        surface = self.__load_image(base_path, 'monsters.png')
        tiles = self.split_surface(surface, (32, 32))

        self.icons[herculeum.config.tiles.HUMAN_FIGHTER] = tiles[3]

        surface = self.__load_image(base_path, 'dungeon.png')
        tiles = self.split_surface(surface, (32, 32))

        self.icons[herculeum.config.tiles.FLOOR_ROCK] = tiles[9]
        self.icons[herculeum.config.tiles.FLOOR_BRICK] = tiles[19]
        self.icons[herculeum.config.tiles.FLOOR_EMPTY] = tiles[263]

        self.icons[herculeum.config.tiles.WALL_ROCK] = tiles[120]
        self.icons[herculeum.config.tiles.WALL_ROCK_DECO_1] = tiles[40]
        self.icons[herculeum.config.tiles.WALL_ROCK_DECO_2] = tiles[46]

        self.icons[herculeum.config.tiles.WALL_GROUND] = tiles[225]

        self.icons[herculeum.config.tiles.PORTAL_STAIRS_DOWN] = tiles[260]
        self.icons[herculeum.config.tiles.PORTAL_STAIRS_UP] = tiles[261]

        surface = self.__load_image(base_path, 'items.png')
        tiles = self.split_surface(surface, (32, 32))
        self.icons[herculeum.config.tiles.ITEM_APPLE] = tiles[0]
        self.icons[herculeum.config.tiles.ITEM_CRYSTAL_SKULL] = tiles[1]

    @logged
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

    @logged
    def get_image(self, id):
        """
        Get image with ID

        :param id: ID number of the image to retrieve
        :type id: int
        :returns: image
        :rtype: QPixmap
        """
        return self.images[id]

    @logged
    def get_icon(self, id):
        """
        Get icon with ID

        :param id: ID number of the icon to retrieve
        :type id: int
        :returns: icon if found, otherwise empty icon
        :rtype: QPixmap
        """
        if id in self.icons:
            return self.icons[id]
        else:
            return self.icons[herculeum.config.tiles.TRANSPARENT]

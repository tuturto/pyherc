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
import logging
import images
import herculeum.config.tiles
import pyherc

from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import QRect

class SurfaceManager:
    """
    Class for managing images and icons
    """
    def __init__(self):
        """
        Default constructor
        """
        self.logger = logging.getLogger('pyherc.gui.surfaceManager')
        self.icons = {}
        self.images = {}
        self.resourcesLoaded = 0

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

    def load_resources(self, base_path):
        """
        Load graphics from files

        :param base_path: path to directory where resources are location
        :type base_path: string
        """
        self.logger.info('loading resources')

        surface = self.__load_image(base_path, 'weapons.png')

        tiles = self.split_surface(surface, (32, 32))

        self.icons[herculeum.config.tiles.ITEM_DAGGER_1] = tiles[3]
        self.icons[herculeum.config.tiles.ITEM_DAGGER_2] = tiles[4]
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

        self.icons[herculeum.config.tiles.CREATURE_RAT_1] = tiles[24]
        self.icons[herculeum.config.tiles.CREATURE_RAT_2] = tiles[25]
        self.icons[herculeum.config.tiles.CREATURE_RAT_3] = tiles[26]
        self.icons[herculeum.config.tiles.CREATURE_RAT_4] = tiles[27]
        self.icons[herculeum.config.tiles.CREATURE_BEETLE_1] = tiles[112]
        self.icons[herculeum.config.tiles.CREATURE_BEETLE_2] = tiles[113]
        self.icons[herculeum.config.tiles.CREATURE_SPIDER_1] = tiles[122]

        surface = self.__load_image(base_path, 'potions.png')
        tiles = self.split_surface(surface, (32, 32))

        self.icons[herculeum.config.tiles.ITEM_POTION_1] = tiles[0]
        self.icons[herculeum.config.tiles.ITEM_POTION_2] = tiles[1]
        self.icons[herculeum.config.tiles.ITEM_POTION_3] = tiles[2]
        self.icons[herculeum.config.tiles.ITEM_POTION_4] = tiles[3]
        self.icons[herculeum.config.tiles.ITEM_POTION_5] = tiles[4]
        self.icons[herculeum.config.tiles.ITEM_POTION_6] = tiles[5]
        self.icons[herculeum.config.tiles.ITEM_POTION_7] = tiles[6]
        self.icons[herculeum.config.tiles.ITEM_POTION_8] = tiles[7]
        self.icons[herculeum.config.tiles.ITEM_POTION_9] = tiles[8]
        self.icons[herculeum.config.tiles.ITEM_POTION_10] = tiles[9]
        self.icons[herculeum.config.tiles.ITEM_POTION_11] = tiles[10]
        self.icons[herculeum.config.tiles.ITEM_POTION_12] = tiles[11]
        self.icons[herculeum.config.tiles.ITEM_POTION_13] = tiles[12]
        self.icons[herculeum.config.tiles.ITEM_POTION_14] = tiles[13]
        self.icons[herculeum.config.tiles.ITEM_POTION_15] = tiles[14]
        self.icons[herculeum.config.tiles.ITEM_POTION_16] = tiles[15]
        self.icons[herculeum.config.tiles.ITEM_POTION_17] = tiles[16]
        self.icons[herculeum.config.tiles.ITEM_POTION_18] = tiles[17]
        self.icons[herculeum.config.tiles.ITEM_POTION_19] = tiles[18]
        self.icons[herculeum.config.tiles.ITEM_POTION_20] = tiles[19]
        self.icons[herculeum.config.tiles.ITEM_POTION_21] = tiles[20]
        self.icons[herculeum.config.tiles.ITEM_POTION_22] = tiles[21]
        self.icons[herculeum.config.tiles.ITEM_POTION_23] = tiles[22]
        self.icons[herculeum.config.tiles.ITEM_POTION_24] = tiles[23]
        self.icons[herculeum.config.tiles.ITEM_POTION_25] = tiles[24]
        self.icons[herculeum.config.tiles.ITEM_POTION_26] = tiles[25]
        self.icons[herculeum.config.tiles.ITEM_POTION_27] = tiles[26]
        self.icons[herculeum.config.tiles.ITEM_POTION_28] = tiles[27]
        self.icons[herculeum.config.tiles.ITEM_POTION_29] = tiles[28]
        self.icons[herculeum.config.tiles.ITEM_POTION_30] = tiles[29]
        self.icons[herculeum.config.tiles.ITEM_POTION_31] = tiles[30]
        self.icons[herculeum.config.tiles.ITEM_POTION_32] = tiles[31]
        self.icons[herculeum.config.tiles.ITEM_POTION_33] = tiles[32]
        self.icons[herculeum.config.tiles.ITEM_POTION_34] = tiles[33]
        self.icons[herculeum.config.tiles.ITEM_POTION_35] = tiles[34]
        self.icons[herculeum.config.tiles.ITEM_POTION_36] = tiles[35]
        self.icons[herculeum.config.tiles.ITEM_POTION_37] = tiles[36]
        self.icons[herculeum.config.tiles.ITEM_POTION_38] = tiles[37]
        self.icons[herculeum.config.tiles.ITEM_POTION_39] = tiles[38]
        self.icons[herculeum.config.tiles.ITEM_POTION_40] = tiles[39]
        self.icons[herculeum.config.tiles.ITEM_POTION_41] = tiles[40]
        self.icons[herculeum.config.tiles.ITEM_POTION_42] = tiles[41]
        self.icons[herculeum.config.tiles.ITEM_POTION_43] = tiles[42]
        self.icons[herculeum.config.tiles.ITEM_POTION_44] = tiles[43]
        self.icons[herculeum.config.tiles.ITEM_POTION_45] = tiles[44]
        self.icons[herculeum.config.tiles.ITEM_POTION_46] = tiles[45]
        self.icons[herculeum.config.tiles.ITEM_POTION_47] = tiles[46]
        self.icons[herculeum.config.tiles.ITEM_POTION_48] = tiles[47]
        self.icons[herculeum.config.tiles.ITEM_POTION_49] = tiles[48]
        self.icons[herculeum.config.tiles.ITEM_POTION_50] = tiles[49]
        self.icons[herculeum.config.tiles.ITEM_POTION_51] = tiles[50]
        self.icons[herculeum.config.tiles.ITEM_POTION_52] = tiles[51]
        self.icons[herculeum.config.tiles.ITEM_POTION_53] = tiles[52]
        self.icons[herculeum.config.tiles.ITEM_POTION_54] = tiles[53]
        self.icons[herculeum.config.tiles.ITEM_POTION_55] = tiles[54]
        self.icons[herculeum.config.tiles.ITEM_POTION_56] = tiles[55]
        self.icons[herculeum.config.tiles.ITEM_POTION_57] = tiles[56]
        self.icons[herculeum.config.tiles.ITEM_POTION_58] = tiles[57]
        self.icons[herculeum.config.tiles.ITEM_POTION_59] = tiles[58]
        self.icons[herculeum.config.tiles.ITEM_POTION_60] = tiles[59]

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

        surface = self.__load_image(base_path, 'characters.png')
        tiles = self.split_surface(surface, (32, 32))
        self.icons[herculeum.config.tiles.HUMAN_FIGHTER] = tiles[3]

        surface = self.__load_image(base_path, 'main_menu.png')
        self.images[images.image_start_menu] = surface
        surface = self.__load_image(base_path, 'play_area.png')
        self.images[images.image_play_area] = surface
        surface = self.__load_image(base_path, 'inventory_menu.png')
        self.images[images.image_inventory_menu] = surface
        surface = self.__load_image(base_path, 'image_marble_slate.png')
        self.images[images.image_end_marble_slate] = surface
        surface = self.__load_image(base_path, 'image_tombstone.png')
        self.images[images.image_end_tombstone] = surface
        surface = self.__load_image(base_path, 'image_console.png')
        self.images[images.image_console] = surface

        surface = self.__load_image(base_path, 'wooden-door.png')
        tiles = self.split_surface(surface, (32, 32))
        self.icons[herculeum.config.tiles.ICON_QUIT_GAME] = tiles[0]

        surface = self.__load_image(base_path, 'cycle.png')
        tiles = self.split_surface(surface, (32, 32))
        self.icons[herculeum.config.tiles.ICON_NEW_GAME] = tiles[0]

        surface = self.__load_image(base_path, 'swap-bag.png')
        tiles = self.split_surface(surface, (32, 32))
        self.icons[herculeum.config.tiles.ICON_INVENTORY] = tiles[0]

        surface = self.__load_image(base_path, 'strong.png')
        tiles = self.split_surface(surface, (32, 32))
        self.icons[herculeum.config.tiles.ICON_CHARACTER] = tiles[0]

        surface = self.__load_image(base_path, 'rune-stone.png')
        tiles = self.split_surface(surface, (32, 32))
        self.icons[herculeum.config.tiles.ICON_HERCULEUM] = tiles[0]

        self.logger.info('resources loaded')

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
        if id in self.icons.keys():
            return self.icons[id]
        else:
            self.logger.warn('icon with id %s not found', id)
            return self.icons[herculeum.config.tiles.FLOOR_EMPTY]

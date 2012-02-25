#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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
import pygame
import logging
import images
import pyherc.data.tiles
import pyherc

class SurfaceManager:
    """
    Class for managing images and icons
    """
    def __init__(self):
        self.logger = logging.getLogger('pyherc.gui.surfaceManager')
        self.icons = {}
        self.images = {}
        self.resourcesLoaded = 0

    def load_surface(self, base_path, image_name):
        """
        Load a file and return corresponding surface object
        @param base_path: directory of the file
        @param image_name: file name
        @returns: Surface
        """
        return pygame.image.load(os.path.join(base_path, image_name))

    def loadResources(self, base_path):
        """
        Load graphics from files
        @param base_path: Path to directory where resources are location
        """

        if self.resourcesLoaded == 0:
            self.logger.info('loading resources')

            surface = self.load_surface(base_path, 'main_menu.png')
            self.images[images.image_start_menu] = surface
            surface = self.load_surface(base_path, 'play_area.png')
            self.images[images.image_play_area] = surface
            surface = self.load_surface(base_path, 'inventory_menu.png')
            self.images[images.image_inventory_menu] = surface
            surface = self.load_surface(base_path, 'image_marble_slate.png')
            self.images[images.image_end_marble_slate] = surface
            surface = self.load_surface(base_path, 'image_tombstone.png')
            self.images[images.image_end_tombstone] = surface
            surface = self.load_surface(base_path, 'image_console.png')
            self.images[images.image_console] = surface

            surface = self.load_surface(base_path, 'character_human_fighter.png')
            self.icons[pyherc.data.tiles.HUMAN_FIGHTER] = surface

            surface = self.load_surface(base_path, 'creature_rat_1.png')
            self.icons[pyherc.data.tiles.CREATURE_RAT_1] = surface
            surface = self.load_surface(base_path, 'creature_rat_2.png')
            self.icons[pyherc.data.tiles.CREATURE_RAT_2] = surface
            surface = self.load_surface(base_path, 'creature_rat_3.png')
            self.icons[pyherc.data.tiles.CREATURE_RAT_3] = surface
            surface = self.load_surface(base_path, 'creature_rat_4.png')
            self.icons[pyherc.data.tiles.CREATURE_RAT_4] = surface
            surface = self.load_surface(base_path, 'creature_beetle_1.png')
            self.icons[pyherc.data.tiles.CREATURE_BEETLE_1] = surface
            surface = self.load_surface(base_path, 'creature_beetle_2.png')
            self.icons[pyherc.data.tiles.CREATURE_BEETLE_2] = surface
            surface = self.load_surface(base_path, 'creature_gargoyle.png')
            self.icons[pyherc.data.tiles.CREATURE_GARGOYLE] = surface

            surface = self.load_surface(base_path, 'floor_stone.png')
            self.icons[pyherc.data.tiles.FLOOR_ROCK] = surface
            surface = self.load_surface(base_path, 'empty.png')
            self.icons[pyherc.data.tiles.FLOOR_EMPTY] = surface

            surface = self.load_surface(base_path, 'wall_stone.png')
            self.icons[pyherc.data.tiles.WALL_ROCK] = surface
            surface = self.load_surface(base_path, 'wall_stone_deco1.png')
            self.icons[pyherc.data.tiles.WALL_ROCK_DECO_1] = surface
            surface = self.load_surface(base_path, 'wall_stone_deco2.png')
            self.icons[pyherc.data.tiles.WALL_ROCK_DECO_2] = surface

            surface = self.load_surface(base_path, 'wall_ground.png')
            self.icons[pyherc.data.tiles.WALL_GROUND] = surface

            surface = self.load_surface(base_path, 'portal_stairs_down.png')
            self.icons[pyherc.data.tiles.PORTAL_STAIRS_DOWN] = surface
            surface = self.load_surface(base_path, 'portal_stairs_up.png')
            self.icons[pyherc.data.tiles.PORTAL_STAIRS_UP] = surface

            surface = self.load_surface(base_path, 'item_apple.png')
            self.icons[pyherc.data.tiles.ITEM_APPLE] = surface
            surface = self.load_surface(base_path, 'item_crystal_skull.png')
            self.icons[pyherc.data.tiles.ITEM_CRYSTAL_SKULL] = surface
            surface = self.load_surface(base_path, 'statue_gargoyle.png')
            self.icons[pyherc.data.tiles.ITEM_GARGOYLE_STATUE] = surface

            surface = self.load_surface(base_path, 'item_dagger_1.png')
            self.icons[pyherc.data.tiles.ITEM_DAGGER_1] = surface
            self.icons[pyherc.data.tiles.ITEM_DAGGER_2] = surface
            surface = self.load_surface(base_path, 'item_morningstar_1.png')
            self.icons[pyherc.data.tiles.ITEM_MORNING_STAR_1] = surface
            surface = self.load_surface(base_path, 'item_morningstar_2.png')
            self.icons[pyherc.data.tiles.ITEM_MORNING_STAR_2] = surface
            surface = self.load_surface(base_path, 'item_short_sword_1.png')
            self.icons[pyherc.data.tiles.ITEM_SHORT_SWORD_1] = surface
            self.icons[pyherc.data.tiles.ITEM_SHORT_SWORD_2] = surface
            surface = self.load_surface(base_path, 'light_mace.png')
            self.icons[pyherc.data.tiles.ITEM_LIGHT_MACE] = surface
            surface = self.load_surface(base_path, 'item_sickle.png')
            self.icons[pyherc.data.tiles.ITEM_SICKLE] = surface
            surface = self.load_surface(base_path, 'light_mace.png')
            self.icons[pyherc.data.tiles.ITEM_CLUB] = surface
            surface = self.load_surface(base_path, 'item_mace.png')
            self.icons[pyherc.data.tiles.ITEM_MACE] = surface
            surface = self.load_surface(base_path, 'item_shortspear.png')
            self.icons[pyherc.data.tiles.ITEM_SHORTSPEAR] = surface
            surface = self.load_surface(base_path, 'item_longspear.png')
            self.icons[pyherc.data.tiles.ITEM_LONGSPEAR] = surface
            surface = self.load_surface(base_path, 'item_spear.png')
            self.icons[pyherc.data.tiles.ITEM_SPEAR] = surface

            #potions
            surface = self.load_surface(base_path, 'item_potion_1.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_1] = surface
            surface = self.load_surface(base_path, 'item_potion_2.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_2] = surface
            surface = self.load_surface(base_path, 'item_potion_3.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_3] = surface
            surface = self.load_surface(base_path, 'item_potion_4.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_4] = surface
            surface = self.load_surface(base_path, 'item_potion_5.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_5] = surface
            surface = self.load_surface(base_path, 'item_potion_6.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_6] = surface
            surface = self.load_surface(base_path, 'item_potion_7.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_7] = surface
            surface = self.load_surface(base_path, 'item_potion_8.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_8] = surface
            surface = self.load_surface(base_path, 'item_potion_9.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_9] = surface
            surface = self.load_surface(base_path, 'item_potion_10.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_10] = surface

            surface = self.load_surface(base_path, 'item_potion_11.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_11] = surface
            surface = self.load_surface(base_path, 'item_potion_12.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_12] = surface
            surface = self.load_surface(base_path, 'item_potion_13.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_13] = surface
            surface = self.load_surface(base_path, 'item_potion_14.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_14] = surface
            surface = self.load_surface(base_path, 'item_potion_15.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_15] = surface
            surface = self.load_surface(base_path, 'item_potion_16.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_16] = surface
            surface = self.load_surface(base_path, 'item_potion_17.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_17] = surface
            surface = self.load_surface(base_path, 'item_potion_18.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_18] = surface
            surface = self.load_surface(base_path, 'item_potion_19.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_19] = surface
            surface = self.load_surface(base_path, 'item_potion_20.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_20] = surface

            surface = self.load_surface(base_path, 'item_potion_21.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_21] = surface
            surface = self.load_surface(base_path, 'item_potion_22.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_22] = surface
            surface = self.load_surface(base_path, 'item_potion_23.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_23] = surface
            surface = self.load_surface(base_path, 'item_potion_24.png')
            self.icons[pyherc.data.tiles.ITEM_POTION_24] = surface

            surface = self.load_surface(base_path, 'trap_magic_1.png')
            self.icons[pyherc.data.tiles.TRAP_MAGIC_1] = surface
            surface = self.load_surface(base_path, 'trap_magic_2.png')
            self.icons[pyherc.data.tiles.TRAP_MAGIC_2] = surface
            surface = self.load_surface(base_path, 'trap_magic_3.png')
            self.icons[pyherc.data.tiles.TRAP_MAGIC_3] = surface

            self.resourcesLoaded = 1
            self.logger.info('resources loaded')
        else:
            self.logger.info('resources already loaded')

    def getImage(self, id):
        """
        Get image with ID

        Args:
            id: ID number of the image to retrieve

        Returns:
            Image
        """
        return self.images[id]

    def getIcon(self, id):
        """
        Get icon with ID

        Args:
            id: ID number of the icon to retrieve

        Returns:
            Icon if found, otherwise empty icon
        """
        if id in self.icons.keys():
            return self.icons[id]
        else:
            self.logger.warn('icon with id %s not found', id)
            return self.icons[pyherc.data.tiles.FLOOR_EMPTY]

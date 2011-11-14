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

import os, sys
import pygame
import logging
import images
import pyHerc.data.tiles
import pyHerc



class SurfaceManager:
    '''
    Class for managing images and icons
    '''
    def __init__(self):
        self.logger = logging.getLogger('pyHerc.gui.surfaceManager')
        self.icons = {}
        self.images = {}
        self.resourcesLoaded = 0

    def loadResources(self):
        """
        Load graphics from files
        """

        if self.resourcesLoaded == 0:
            self.logger.info('loading resources')

            surface = pygame.image.load('C:/programming/pyHack/resources/main_menu.png')
            self.images[images.image_start_menu] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/menu_arrow.png')
            self.images[images.image_start_menu_arrow] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/play_area.png')
            self.images[images.image_play_area] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/inventory_menu.png')
            self.images[images.image_inventory_menu] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/image_marble_slate.png')
            self.images[images.image_end_marble_slate] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/image_tombstone.png')
            self.images[images.image_end_tombstone] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/image_console.png')
            self.images[images.image_console] = surface

            surface = pygame.image.load('C:/programming/pyHack/resources/character_human_fighter.png')
            self.icons[pyHerc.data.tiles.HUMAN_FIGHTER] = surface

            surface = pygame.image.load('C:/programming/pyHack/resources/creature_rat_1.png')
            self.icons[pyHerc.data.tiles.CREATURE_RAT_1] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/creature_rat_2.png')
            self.icons[pyHerc.data.tiles.CREATURE_RAT_2] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/creature_rat_3.png')
            self.icons[pyHerc.data.tiles.CREATURE_RAT_3] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/creature_rat_4.png')
            self.icons[pyHerc.data.tiles.CREATURE_RAT_4] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/creature_beetle_1.png')
            self.icons[pyHerc.data.tiles.CREATURE_BEETLE_1] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/creature_beetle_2.png')
            self.icons[pyHerc.data.tiles.CREATURE_BEETLE_2] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/creature_gargoyle.png')
            self.icons[pyHerc.data.tiles.CREATURE_GARGOYLE] = surface

            surface = pygame.image.load('C:/programming/pyHack/resources/floor_stone.png')
            self.icons[pyHerc.data.tiles.FLOOR_ROCK] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/empty.png')
            self.icons[pyHerc.data.tiles.FLOOR_EMPTY] = surface

            surface = pygame.image.load('C:/programming/pyHack/resources/wall_stone.png')
            self.icons[pyHerc.data.tiles.WALL_ROCK] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/wall_stone_deco1.png')
            self.icons[pyHerc.data.tiles.WALL_ROCK_DECO_1] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/wall_stone_deco2.png')
            self.icons[pyHerc.data.tiles.WALL_ROCK_DECO_2] = surface

            surface = pygame.image.load('C:/programming/pyHack/resources/wall_ground.png')
            self.icons[pyHerc.data.tiles.WALL_GROUND] = surface

            surface = pygame.image.load('C:/programming/pyHack/resources/portal_stairs_down.png')
            self.icons[pyHerc.data.tiles.PORTAL_STAIRS_DOWN] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/portal_stairs_up.png')
            self.icons[pyHerc.data.tiles.PORTAL_STAIRS_UP] = surface

            surface = pygame.image.load('C:/programming/pyHack/resources/item_apple.png')
            self.icons[pyHerc.data.tiles.ITEM_APPLE] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_crystal_skull.png')
            self.icons[pyHerc.data.tiles.ITEM_CRYSTAL_SKULL] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/statue_gargoyle.png')
            self.icons[pyHerc.data.tiles.ITEM_GARGOYLE_STATUE] = surface

            #TODO: correct graphics
            surface = pygame.image.load('C:/programming/pyHack/resources/item_dagger_1.png')
            self.icons[pyHerc.data.tiles.ITEM_DAGGER_1] = surface
            self.icons[pyHerc.data.tiles.ITEM_DAGGER_2] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_morningstar_1.png')
            self.icons[pyHerc.data.tiles.ITEM_MORNING_STAR_1] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_morningstar_2.png')
            self.icons[pyHerc.data.tiles.ITEM_MORNING_STAR_2] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_short_sword_1.png')
            self.icons[pyHerc.data.tiles.ITEM_SHORT_SWORD_1] = surface
            self.icons[pyHerc.data.tiles.ITEM_SHORT_SWORD_2] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/light_mace.png')
            self.icons[pyHerc.data.tiles.ITEM_LIGHT_MACE] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_sickle.png')
            self.icons[pyHerc.data.tiles.ITEM_SICKLE] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/light_mace.png')
            self.icons[pyHerc.data.tiles.ITEM_CLUB] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_mace.png')
            self.icons[pyHerc.data.tiles.ITEM_MACE] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_shortspear.png')
            self.icons[pyHerc.data.tiles.ITEM_SHORTSPEAR] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_longspear.png')
            self.icons[pyHerc.data.tiles.ITEM_LONGSPEAR] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_spear.png')
            self.icons[pyHerc.data.tiles.ITEM_SPEAR] = surface

            #potions
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_1.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_1] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_2.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_2] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_3.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_3] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_4.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_4] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_5.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_5] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_6.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_6] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_7.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_7] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_8.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_8] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_9.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_9] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_10.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_10] = surface

            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_11.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_11] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_12.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_12] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_13.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_13] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_14.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_14] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_15.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_15] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_16.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_16] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_17.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_17] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_18.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_18] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_19.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_19] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_20.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_20] = surface

            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_21.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_21] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_22.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_22] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_23.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_23] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_24.png')
            self.icons[pyHerc.data.tiles.ITEM_POTION_24] = surface

            surface = pygame.image.load('C:/programming/pyHack/resources/trap_magic_1.png')
            self.icons[pyHerc.data.tiles.TRAP_MAGIC_1] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/trap_magic_2.png')
            self.icons[pyHerc.data.tiles.TRAP_MAGIC_2] = surface
            surface = pygame.image.load('C:/programming/pyHack/resources/trap_magic_3.png')
            self.icons[pyHerc.data.tiles.TRAP_MAGIC_3] = surface

            self.resourcesLoaded = 1
            self.logger.info('resources loaded')
        else:
            self.logger.info('resources already loaded')

    def getImage(self, id):
        return self.images[id]

    def getIcon(self, id):
        if id in self.icons.keys():
            return self.icons[id]
        else:
            self.logger.warn('icon with id %s not found', id)
            return self.icons[pyHerc.data.tiles.FLOOR_EMPTY]

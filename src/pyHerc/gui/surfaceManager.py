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
from pygame.locals import *

__logger = logging.getLogger('pyHerc.gui.surfaceManager')
__icons = {}
__images = {}
__resourcesLoaded = 0

def loadResources():
    """
    Load graphics from files
    """
    global __resourcesLoaded
    global __images
    global __icons
    global __logger

    if __resourcesLoaded == 0:
        __logger.info('loading resources')

        surface = pygame.image.load('C:/programming/pyHack/resources/main_menu.png')
        __images[images.image_start_menu] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/menu_arrow.png')
        __images[images.image_start_menu_arrow] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/play_area.png')
        __images[images.image_play_area] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/inventory_menu.png')
        __images[images.image_inventory_menu] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/image_marble_slate.png')
        __images[images.image_end_marble_slate] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/image_tombstone.png')
        __images[images.image_end_tombstone] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/image_console.png')
        __images[images.image_console] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/character_human_fighter.png')
        __icons[pyHerc.data.tiles.human_fighter] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/creature_rat_1.png')
        __icons[pyHerc.data.tiles.creature_rat_1] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/creature_rat_2.png')
        __icons[pyHerc.data.tiles.creature_rat_2] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/creature_rat_3.png')
        __icons[pyHerc.data.tiles.creature_rat_3] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/creature_rat_4.png')
        __icons[pyHerc.data.tiles.creature_rat_4] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/creature_beetle_1.png')
        __icons[pyHerc.data.tiles.creature_beetle_1] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/creature_beetle_2.png')
        __icons[pyHerc.data.tiles.creature_beetle_2] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/floor_stone.png')
        __icons[pyHerc.data.tiles.floor_rock] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/empty.png')
        __icons[pyHerc.data.tiles.floor_empty] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/wall_stone.png')
        __icons[pyHerc.data.tiles.wall_rock] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/wall_stone_deco1.png')
        __icons[pyHerc.data.tiles.wall_rock_deco_1] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/wall_stone_deco2.png')
        __icons[pyHerc.data.tiles.wall_rock_deco_2] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/wall_ground.png')
        __icons[pyHerc.data.tiles.wall_ground] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/portal_stairs_down.png')
        __icons[pyHerc.data.tiles.portal_stairs_down] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/portal_stairs_up.png')
        __icons[pyHerc.data.tiles.portal_stairs_up] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/item_apple.png')
        __icons[pyHerc.data.tiles.item_apple] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_crystal_skull.png')
        __icons[pyHerc.data.tiles.item_crystal_skull] = surface

        #TODO: correct graphics
        surface = pygame.image.load('C:/programming/pyHack/resources/item_dagger_1.png')
        __icons[pyHerc.data.tiles.item_dagger_1] = surface
        __icons[pyHerc.data.tiles.item_dagger_2] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_morningstar_1.png')
        __icons[pyHerc.data.tiles.item_morning_star_1] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_morningstar_2.png')
        __icons[pyHerc.data.tiles.item_morning_star_2] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_short_sword_1.png')
        __icons[pyHerc.data.tiles.item_short_sword_1] = surface
        __icons[pyHerc.data.tiles.item_short_sword_2] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/light_mace.png')
        __icons[pyHerc.data.tiles.item_light_mace] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_sickle.png')
        __icons[pyHerc.data.tiles.item_sickle] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/light_mace.png')
        __icons[pyHerc.data.tiles.item_club] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_mace.png')
        __icons[pyHerc.data.tiles.item_mace] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_shortspear.png')
        __icons[pyHerc.data.tiles.item_shortspear] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_longspear.png')
        __icons[pyHerc.data.tiles.item_longspear] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_spear.png')
        __icons[pyHerc.data.tiles.item_spear] = surface

        #potions
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_1.png')
        __icons[pyHerc.data.tiles.item_potion_1] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_2.png')
        __icons[pyHerc.data.tiles.item_potion_2] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_3.png')
        __icons[pyHerc.data.tiles.item_potion_3] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_4.png')
        __icons[pyHerc.data.tiles.item_potion_4] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_5.png')
        __icons[pyHerc.data.tiles.item_potion_5] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_6.png')
        __icons[pyHerc.data.tiles.item_potion_6] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_7.png')
        __icons[pyHerc.data.tiles.item_potion_7] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_8.png')
        __icons[pyHerc.data.tiles.item_potion_8] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_9.png')
        __icons[pyHerc.data.tiles.item_potion_9] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_10.png')
        __icons[pyHerc.data.tiles.item_potion_10] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_11.png')
        __icons[pyHerc.data.tiles.item_potion_11] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_12.png')
        __icons[pyHerc.data.tiles.item_potion_12] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_13.png')
        __icons[pyHerc.data.tiles.item_potion_13] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_14.png')
        __icons[pyHerc.data.tiles.item_potion_14] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_15.png')
        __icons[pyHerc.data.tiles.item_potion_15] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_16.png')
        __icons[pyHerc.data.tiles.item_potion_16] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_17.png')
        __icons[pyHerc.data.tiles.item_potion_17] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_18.png')
        __icons[pyHerc.data.tiles.item_potion_18] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_19.png')
        __icons[pyHerc.data.tiles.item_potion_19] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_20.png')
        __icons[pyHerc.data.tiles.item_potion_20] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_21.png')
        __icons[pyHerc.data.tiles.item_potion_21] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_22.png')
        __icons[pyHerc.data.tiles.item_potion_22] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_23.png')
        __icons[pyHerc.data.tiles.item_potion_23] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_potion_24.png')
        __icons[pyHerc.data.tiles.item_potion_24] = surface


        __resourcesLoaded = 1
        __logger.info('resources loaded')
    else:
        __logger.info('resources already loaded')

def getImage(id):
    return __images[id]

def getIcon(id):
    if id in __icons.keys():
        return __icons[id]
    else:
        __logger.warn('icon with id %s not found', id)
        return __icons[pyHerc.data.tiles.floor_empty]

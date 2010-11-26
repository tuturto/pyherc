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

        surface = pygame.image.load('C:/programming/pyHack/resources/character_human_fighter.png')
        __icons[pyHerc.data.tiles.human_fighter] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/creature_rat.png')
        __icons[pyHerc.data.tiles.creature_rat] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/floor_stone.png')
        __icons[pyHerc.data.tiles.floor_rock] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/empty.png')
        __icons[pyHerc.data.tiles.floor_empty] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/wall_stone.png')
        __icons[pyHerc.data.tiles.wall_rock] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/portal_stairs.png')
        __icons[pyHerc.data.tiles.portal_stairs] = surface

        surface = pygame.image.load('C:/programming/pyHack/resources/item_apple.png')
        __icons[pyHerc.data.tiles.item_apple] = surface
        surface = pygame.image.load('C:/programming/pyHack/resources/item_crystal_skull.png')
        __icons[pyHerc.data.tiles.item_crystal_skull] = surface

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
        return __icons[pyHerc.data.tiles.floor_empty]

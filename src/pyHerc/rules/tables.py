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
import logging
import pyHerc.data.model
from pyHerc.data import tiles

__initialised = 0
food = {}
specialItems = {}
weapons = {}
characters = {}
creatures = {}
kits = {}
sizeModifier = {}
attributeModifier = []

def loadTables():
    """
    Initialise tables
    """
    global food
    global specialItems
    global creatures
    global sizeModifier
    global attributeModifier
    global __initialised

    if __initialised:
        return

    food['apple'] = {'name' : 'apple',
                                'icon' : pyHerc.data.tiles.item_apple}

    specialItems['crystal skull'] = {'name' : 'Crystal skull',
                                                        'questItem' : 1,
                                                        'icon' : pyHerc.data.tiles.item_crystal_skull}

    creatures['rat'] = {'name' : 'rat',
                                    'str' : 4,
                                    'dex' : 12,
                                    'con' : 4,
                                    'int' : 2,
                                    'wis' : 4,
                                    'cha' : 4,
                                    'hp' : 2,
                                    'speed' : 2,
                                    'icon' : pyHerc.data.tiles.creature_rat,
                                    'attack' : '1d4'}

    sizeModifier = {'colossal' :  -8, 'gargantuan' : -4, 'huge' : -2, 'large' : -1,
                            'medium' : 0, 'small' : 1, 'tiny' : 2, 'diminutive' : 4, 'fine' : 8}

    attributeModifier = [-6, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

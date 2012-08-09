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
Various rules used in character generation
"""

import logging
from pyherc.data import Character, WeaponProficiency, EffectsCollection
import herculeum.config.tiles

__logger = logging.getLogger('pyherc.rules.character')

race_stats = None
kit_stats = None

def initialise_stat_tables():
    """
    Initialise stat tables
    """
    global race_stats
    global kit_stats
    global __logger

    __logger.info('initialising stat tables')

    race_stats = {}
    kit_stats = {}

    temp_race = {}
    temp_race['body'] = 7
    temp_race['finesse'] = 7
    temp_race['mind'] = 7
    temp_race['hp'] = 7
    temp_race['speed'] = 3
    race_stats['human'] = temp_race

    temp_kit = {}
    temp_kit['body'] = -1
    temp_kit['finesse'] = 0
    temp_kit['mind'] = 1
    temp_kit['hp'] = 2
    temp_kit['speed'] = - 0.5
    kit_stats['fighter'] = temp_kit

    __logger.info('stat tables initialised')

def create_character(race, kit, model):
    """
    Creates a new character with given race and kit
    """
    global race_stats
    global kit_stats
    global __logger

    if race_stats == None:
        initialise_stat_tables()

    temp_race = race_stats[race]
    temp_kit = kit_stats[kit]

    new_character = Character(model,
                              EffectsCollection())
    new_character.body = temp_race['body'] + temp_kit['body']
    new_character.finesse = temp_race['finesse'] + temp_kit['finesse']
    new_character.mind = temp_race['mind'] + temp_kit['mind']
    new_character.hit_points = temp_race['hp'] + temp_kit['hp']
    new_character.max_hp = new_character.hit_points
    new_character.speed = temp_race['speed'] + temp_kit['speed']
    new_character.size = 'medium'
    new_character.attack = 3

    new_character.feats.append(WeaponProficiency('simple'))
    new_character.icon = herculeum.config.tiles.HUMAN_FIGHTER

    return new_character

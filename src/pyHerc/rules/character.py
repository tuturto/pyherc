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

__logger = logging.getLogger('pyHerc.rules.character')

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
    temp_race['str'] = 10
    temp_race['dex'] = 10
    temp_race['con'] = 10
    temp_race['int'] = 10
    temp_race['wis'] = 10
    temp_race['cha'] = 10
    temp_race['hp'] = 10
    temp_race['speed'] = 3
    race_stats['human'] = temp_race

    temp_kit = {}
    temp_kit['str'] = 2
    temp_kit['dex'] = 0
    temp_kit['con'] = 2
    temp_kit['int'] = -2
    temp_kit['wis'] = -1
    temp_kit['cha'] = -1
    temp_kit['hp'] = 2
    temp_kit['speed'] = - 0.5
    kit_stats['fighter'] = temp_kit

    __logger.info('stat tables initialised')

def create_character(race, kit):
    """
    Creates a new character with given race and kit
    """
    global race_stats
    global kit_stats
    global __logger
    #TODO: change to use rules.tables
    __logger.debug('creating a new character: ' + race + " " + kit)

    if race_stats == None:
        initialise_stat_tables()

    temp_race = race_stats[race]
    temp_kit = kit_stats[kit]

    new_character = pyHerc.data.model.Character()
    new_character.str = temp_race['str'] + temp_kit['str']
    new_character.dex = temp_race['dex'] + temp_kit['dex']
    new_character.con = temp_race['con'] + temp_kit['con']
    new_character.wis = temp_race['wis'] + temp_kit['wis']
    new_character.int = temp_race['int'] + temp_kit['int']
    new_character.cha = temp_race['cha'] + temp_kit['cha']
    new_character.hp = temp_race['hp'] + temp_kit['hp']
    new_character.maxHp = new_character.hp
    new_character.speed = temp_race['speed'] + temp_kit['speed']
    #TODO: implement properly
    new_character.size = 'medium'
    new_character.attack = '1d3'

    #TODO: get from a factory
    new_character.feats.append(
                              pyHerc.data.model.WeaponProficiency('simple'))
    new_character.icon = __get_icon(race, kit)

    return new_character

def __get_icon(race, kit):
    #TODO: implement
    return pyHerc.data.tiles.human_fighter

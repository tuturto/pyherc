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
Various rules used in character generation
"""

import logging
import pyherc.data.model

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

def create_character(race, kit, action_factory):
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

    new_character = pyherc.data.model.Character(action_factory)
    new_character.set_body(temp_race['body'] + temp_kit['body'])
    new_character.set_finesse(temp_race['finesse'] + temp_kit['finesse'])
    new_character.set_mind(temp_race['mind'] + temp_kit['mind'])
    new_character.hit_points = temp_race['hp'] + temp_kit['hp']
    new_character.max_hp = new_character.hit_points
    new_character.speed = temp_race['speed'] + temp_kit['speed']
    #TODO: implement properly
    new_character.size = 'medium'
    new_character.attack = 3

    #TODO: get from a factory
    new_character.feats.append(
                              pyherc.data.model.WeaponProficiency('simple'))
    new_character.icon = __get_icon(race, kit)

    return new_character

def __get_icon(race, kit):
    """
    Get icon to represent race and kit

    Args:
        race: name of the race
        kit: name of the kit

    Returns:
        Icon
    """
    #TODO: implement
    return pyherc.data.tiles.HUMAN_FIGHTER

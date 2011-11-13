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

__logger = logging.getLogger('pyHerc.rules.ending')

def check_result(model):
    """
    Check how the game actually ended
    @param model: model containing play data
    @return: dictionary containing following keys: reason, score, dead reason
    @note: valid reasons: dead, escaped, victory, quit
    @note: dead reason will contain reason of death, if player died
    """
    result = {}
    if model.player.hit_points <= 0:
        #player has died
        result['reason'] = 'dead'
        #TODO: implement correct reason
        result['dead reason'] = 'died while adventuring'
    elif model.player.level == None:
        #escaped or victory
        for item in model.player.inventory:
            if item.name == 'crystal skull':
                #victory
                result['reason'] = 'victory'
        if not 'reason' in result.keys():
            #escaped
            result['reason'] = 'escaped'
    else:
        result['reason'] = 'quit'

    result['score'] = get_ending_score(model)

    return result

def get_ending_score(model):
    """
    Calculate ending score
    @param model: model containing play data
    @return: score
    """
    #TODO: implement scoring
    return 0

def check_dying(model, character, deathParams):
    """
    Check if cracter is dead and should be dealt with
    @param mode: model to use
    @param character: character to check
    @param deathParams: parameters detailing the death condition
    """
    assert character != None
    if character.hit_points <= 0:
        __logger.debug(character.__str__() + ' has died')
        event = {}
        event['type'] = 'death'
        event['character'] = character
        event['location'] = character.location
        event['level'] = character.level
        model.raise_event(event)
        #TODO: implement leaving corpse
        if character != model.player:
            character.level.remove_creature(character)
        else:
            model.end_condition = 1

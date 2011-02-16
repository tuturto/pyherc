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

def checkResult(model):
    """
    Check how the game actually ended
    @param model: model containing play data
    @return: dictionary containing following keys: reason, score, dead reason
    @note: valid reasons: dead, escaped, victory, quit
    @note: dead reason will contain reason of death, if player died
    """
    result = {}
    if model.player.hp <= 0:
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

    result['score'] = getEndingScore(model)

    return result

def getEndingScore(model):
    """
    Calculate ending score
    @param model: model containing play data
    @return: score
    """
    #TODO: implement scoring
    return 0

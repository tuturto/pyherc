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

import logging
import math

__logger = logging.getLogger('pyHerc.rules.los')

def get_light_matrix(model, character, distance = 7):
    '''
    Calculate light matrix for given character
    @param model: model to use
    @param character: character whose light matrix should be calculated
    @param distance: optional range for light source
    '''
    assert model != None
    assert character != None

    level = character.level
    light_matrix = []

    for loc_x in range(-12, 13):
        temp_row = []
        for loc_y in range(-7, 8):
            if loc_x * loc_x + loc_y * loc_y > distance * distance:
                temp_row.append(0)
            else:
                temp_row.append(1)
        light_matrix.append(temp_row)

    return light_matrix

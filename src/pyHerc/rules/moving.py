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
import pyHerc.data.tiles

__logger = logging.getLogger('pyHerc.rules.moving')

def move(model, character, direction):
    """
    moves character to specified direction
    Params:
        model : model of the world
        character : character to move
        direction : direction to move (1: north, 3: east, 9 up, 10 down)
    Remarks:
        Character does not move if it's not possible
    """
    assert(not model == None)
    assert(not character == None)
    assert(direction >= 1 and direction <= 10)

    __logger.debug('character ' + character.name +
                            ' moving from ' + character.location.__str__() +
                            ' to direction: ' + direction.__str__())

    if canMove(model, character, direction):
        character.location = __calculateNewLocation(character.location, direction)
        #TODO: implement walking stairs

    __logger.debug('move finished at ' + character.location.__str__())

def canMove(model, character, direction):
    """
    checks if character can move to specific direction
    Params:
        model : model of the world
        character : character to move
        direction : direction to move (1: north, 3: east, 9 up, 10 down)
    Returns:
        1 / 0 depending if the character can move or not
    """
    assert(not model == None)
    assert(not character == None)
    assert(direction >= 1 and direction <= 10)

    newLocation = __calculateNewLocation(character.location, direction)

    if character.level.walls[newLocation[0]][newLocation[1]] == pyHerc.data.tiles.wall_empty:
        return 1
    else:
        return 0

def __calculateNewLocation(location, direction):
    """
    Calculate new location if moving from old to certain direction
    Params:
        location : starting location
        direction : direction to move
    """
    assert(not location == None)
    assert(direction >= 1 and direction <= 10)

    if direction == 1:
        newLocation = (location[0], location[1] - 1)
    elif direction == 2:
        newLocation = (location[0] + 1, location[1] - 1)
    elif direction == 3:
        newLocation = (location[0] + 1, location[1])
    elif direction == 4:
        newLocation = (location[0] + 1, location[1] + 1)
    elif direction == 5:
        newLocation = (location[0], location[1] + 1)
    elif direction == 6:
        newLocation = (location[0] - 1, location[1] + 1)
    elif direction == 7:
        newLocation = (location[0] - 1, location[1])
    elif direction == 8:
        newLocation = (location[0] - 1, location[1] - 1)
    #TODO: implement walking stairs

    return newLocation

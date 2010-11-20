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
        direction : direction to move (1: north, 3: east, 9 enter portal)
    Remarks:
        Character does not move if it's not possible
    """
    assert(not model == None)
    assert(not character == None)
    assert(direction >= 1 and direction <= 10)

    __logger.debug('character ' + character.name +
                            ' moving from ' + character.location.__str__() +
                            ' to direction: ' + direction.__str__())

    moveData = checkMove(model, character, direction)

    if moveData['ok'] == 1:
        character.location = moveData['location']
        character.level = moveData['level']

    __logger.debug('move finished at ' + character.location.__str__())

def checkMove(model, character, direction):
    """
    checks if character can move to specific direction
    Params:
        model : model of the world
        character : character to move
        direction : direction to move (1: north, 3: east, 9 enter portal)
    Returns:
        dictionary with following keys:
            location : new location
            level : new level
            ok : 1 / 0 depending if move is ok
    """
    assert(not model == None)
    assert(not character == None)
    assert(direction >= 1 and direction <= 9)

    locationData = __calculateNewLocation(character, direction)
    newLocation = locationData['location']
    newLevel = locationData['level']

    if newLevel != None:
        if newLevel.walls[newLocation[0]][newLocation[1]] == pyHerc.data.tiles.wall_empty:
            locationData['ok'] = 1
        else:
            locationData['ok'] = 0
    else:
        locationData['ok'] = 0

    return locationData

def __calculateNewLocation(character, direction):
    """
    Calculate new location if moving from old to certain direction
    Params:
        character : character who is about to move
        direction : direction to move
    Returns:
        dictionary with keys:
            level : level where move ends
            location : location within that level
    """
    assert(not character == None)
    assert(direction >= 1 and direction <= 9)

    location = character.location
    newLevel = character.level

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
    elif direction == 9:
        portal = newLevel.getPortalAt(location)
        if portal != None:
            newLevel = portal.otherEnd.level
            newLocation = portal.otherEnd.location
        else:
            newLevel = None
            newLocation = None

    return {'location':newLocation,
                'level':newLevel}

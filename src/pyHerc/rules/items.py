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

__logger = logging.getLogger('pyHerc.rules.items')

def pickUp(model, character, item):
    """
    Pick up an item
    Parameters:
        model : model to use
        character : character picking up the item
        item : item to be picked up
    """
    assert(not model == None)
    assert(not character == None)
    assert(not item == None)

    if (not item.location == character.location):
        return

    if (not item in character.level.items):
        return

    character.level.items.remove(item)
    character.inventory.append(item)

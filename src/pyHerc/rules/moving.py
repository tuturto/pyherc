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
import time
import pyHerc.data.model
import pyHerc.data.tiles

__logger = logging.getLogger('pyHerc.rules.moving')

def deactivate(model, character):
    '''
    Deactivates a character, causing it to hide
    @param model: model to use
    @param character: character to hide
    '''
    __logger.debug('deactivating character: ' + character.__str__())
    item = character.get_mimic_item()
    character.set_mimic_item(None)
    level = character.level
    location = character.get_location()

    level.add_item(item, location)
    level.remove_creature(character)
    __logger.debug('character deactivated')

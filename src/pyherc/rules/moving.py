#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Module for moving related actions
"""

import logging

__logger = logging.getLogger('pyherc.rules.moving')

def deactivate(model, character):
    """
    Deactivates a character, causing it to hide
    @param model: model to use
    @param character: character to hide
    """
    item = character.get_mimic_item()
    character.set_mimic_item(None)
    level = character.level
    location = character.get_location()

    level.add_item(item, location)
    level.remove_creature(character)

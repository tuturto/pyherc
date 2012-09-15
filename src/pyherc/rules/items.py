#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Rules for manipulating items

.. warning:: This code will be eventually replaced by action sub system
"""

import logging

logger = logging.getLogger('pyherc.rules.items')

def wield(model, character, item, dual_wield = False):
    """
    Wield a weapon
    :param model: model to use
    :type model: Model
    :param character: character trying to wield the weapon
    :type character: Character
    :param item: weapon to wield
    :type item: Item
    :param dual_wield: should character perform dual wield
    :type dual_wield: Boolean

    .. warning:: This code will be eventually replaced by action sub system
    """

    if character.weapon == None:
        character.weapon = item

def unwield(model, character, item, instant = False):
    """
    Unwield an item

    :param model: model to use
    :type model: Model
    :param character: character unwielding an item
    :type character: Character
    :param item: item to unwield
    :type item: Item
    :param instant: is this instant action, default False
    :type instant: Boolean
    :returns: True if unwield was succesfull, False otherwise
    :rtype: Boolean

    .. warning:: This code will be eventually replaced by action sub system
    """
    if character.weapon == item:
        character.weapon = None

    return True

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
Module handling time functions
"""

import logging

__logger = logging.getLogger('pyherc.rules.time')

def get_next_creature(model):
    """
    Get the character who is next to take action

    Returns
        Character to act next
    """
    assert(model != None)

    level = model.player.level
    creatures = level.creatures

    assert len(creatures) != 0
    assert model.player in level.creatures

    while 1:
        for creature in creatures:
            if creature.tick <= 0:
                return creature

        for creature in creatures:
            creature.tick = creature.tick - 1
            for effect in creature.active_effects:
                effect.tick = effect.tick - 1
                if effect.tick == 0:
                    effect.trigger()

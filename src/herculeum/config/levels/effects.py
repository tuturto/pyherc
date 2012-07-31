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
module for configuring effects
"""
from pyherc.rules.effects import Heal, Poison

def init_effects():
    """
    Initialise common effects

    :returns: effect configuration
    """
    config = []

    config.append(('cure minor wounds',
                   {'type': Heal,
                    'duration': 20,
                    'frequency': 5,
                    'tick': 2,
                    'healing': 1}))

    config.append(('cure medium wounds',
                   {'type': Heal,
                    'duration': 20,
                    'frequency': 5,
                    'tick': 2,
                    'healing': 2}))

    config.append(('minor poison',
                   {'type': Poison,
                    'duration': 240,
                    'frequency': 60,
                    'tick': 60,
                    'damage': 1}))

    return config

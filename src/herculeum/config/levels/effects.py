# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
from pyherc.data.effects import DamageEffect, Heal, Poison


def init_effects(context):
    """
    Initialise common effects

    :returns: effect configuration
    """
    surface_manager = context.surface_manager
    config = []

    config.append(('cure minor wounds',
                   {'type': Heal,
                    'duration': 20,
                    'frequency': 5,
                    'tick': 2,
                    'healing': 1,
                    'icon': surface_manager.add_icon('cure minor wounds',
                                                     ':minor_healing.png',
                                                     ''),
                    'title': 'Cure minor wounds',
                    'description': 'Cures small amount of damage'}))

    config.append(('cure medium wounds',
                   {'type': Heal,
                    'duration': 20,
                    'frequency': 5,
                    'tick': 2,
                    'healing': 2,
                    'icon': surface_manager.add_icon('cure medium wounds',
                                                     ':moderate_healing.png',
                                                     ''),
                    'title': 'Cure medium wounds',
                    'description': 'Cures medium amount of damage'}))

    config.append(('minor poison',
                   {'type': Poison,
                    'duration': 240,
                    'frequency': 60,
                    'tick': 60,
                    'damage': 1,
                    'icon': surface_manager.add_icon('minor poison',
                                                     ':minor_poison.png',
                                                     ''),
                    'title': 'Minor poison',
                    'description': 'Causes minor amount of damage'}))

    config.append(('cause wound',
                   {'type': DamageEffect,
                    'duration': None,
                    'frequency': None,
                    'tick': None,
                    'damage': 5,
                    'damage_type': 'magic',
                    'icon': surface_manager.add_icon('minor poison',
                                                     ':minor_poison.png',
                                                     ''),
                    'title': 'Wound',
                    'description': 'Instant magical damage'}))


    config.append(('major fire damage',
                   {'type': DamageEffect,
                    'duration': None,
                    'frequency': None,
                    'tick': None,
                    'damage': 12,
                    'damage_type': 'fire',
                    'icon': surface_manager.add_icon('minor poison',
                                                     ':minor_poison.png',
                                                     ''),
                    'title': 'Major fire damage',
                    'description': 'Causes major amount of fire damage'}))

    config.append(('fire',
                   {'type': DamageEffect,
                   'duration': 20,
                   'frequency': 2,
                   'tick': 5,
                   'damage': 1,
                   'damage_type': 'fire',
                   'icon': surface_manager.add_icon('fire effect',
                                                    ':fire_effect.png',
                                                    ''),
                   'title': 'Fire',
                   'description': 'You are on fire!'}))

    return config

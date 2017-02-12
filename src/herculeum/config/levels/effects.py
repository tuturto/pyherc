# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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

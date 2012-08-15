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
module for configuring catacombs
"""
from pyherc.generators import ItemConfigurations
from pyherc.generators import ItemConfiguration, WeaponConfiguration
from pyherc.data.effects import EffectHandle

def init_items():
    """
    Initialise common items

    :returns: item configurations
    :rtype: [ItemConfiguration]
    """
    config = []

    config.append(
                  ItemConfiguration(name = 'apple',
                                    cost = 1,
                                    weight = 1,
                                    icons = [501],
                                    types = ['food'],
                                    rarity = 'common'))

    config.append(
                  ItemConfiguration(name = 'dagger',
                                    cost = 2,
                                    weight = 1,
                                    icons = [602, 603],
                                    types = ['weapon',
                                               'light weapon',
                                               'melee',
                                               'simple weapon'],
                                    rarity = 'common',
                                    weapon_configration = WeaponConfiguration(
                                            damage = 2,
                                            critical_range = 11,
                                            critical_damage = 2,
                                            damage_types = ['piercing',
                                                            'slashing'],
                                            weapon_class = 'simple')))

    config.append(
                  ItemConfiguration(name = 'healing potion',
                                    cost = 150,
                                    weight = 1,
                                    icons = [701],
                                    types = ['potion'],
                                    rarity = 'rare',
                                    effect_handles = [EffectHandle(
                                            trigger = 'on drink',
                                            effect = 'cure medium wounds',
                                            parameters = None,
                                            charges = 1)]))

    return config

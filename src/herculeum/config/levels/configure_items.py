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
from pyherc.generators import ArmourConfiguration
from pyherc.data.effects import EffectHandle

def init_items(context):
    """
    Initialise common items

    :returns: item configurations
    :rtype: [ItemConfiguration]
    """
    surface_manager = context.surface_manager
    config = []

    config.append(
                  ItemConfiguration(name = 'apple',
                                    cost = 1,
                                    weight = 1,
                                    icons = [surface_manager.add_icon('apple', ':apple.png')],
                                    types = ['food'],
                                    rarity = 'common'))

    config.append(
                  ItemConfiguration(name = 'dagger',
                                    cost = 2,
                                    weight = 1,
                                    icons = [surface_manager.add_icon('dagger', ':dagger.png')],
                                    types = ['weapon',
                                               'light weapon',
                                               'melee',
                                               'simple weapon'],
                                    rarity = 'common',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(2, 'piercing')],
                                            critical_range = 11,
                                            critical_damage = 2,
                                            weapon_class = 'simple')))

    config.append(
                  ItemConfiguration(name = 'sword',
                                    cost = 6,
                                    weight = 4,
                                    icons = [surface_manager.add_icon('sword', ':stiletto.png')],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'martial weapon'],
                                    rarity = 'uncommon',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(2, 'piercing'),
                                                      (2, 'slashing')],
                                            critical_range = 12,
                                            critical_damage = 2,
                                            weapon_class = 'martial')))

    config.append(
                  ItemConfiguration(name = 'axe',
                                    cost = 6,
                                    weight = 4,
                                    icons = [surface_manager.add_icon('axe', ':battle-axe.png')],
                                    types = ['weapon',
                                             'two-handed',
                                             'melee',
                                             'martial weapon'],
                                    rarity = 'uncommon',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(2, 'crushing'),
                                                      (2, 'slashing')],
                                            critical_range = 12,
                                            critical_damage = 2,
                                            weapon_class = 'martial')))

    config.append(
                  ItemConfiguration(name = 'club',
                                    cost = 6,
                                    weight = 4,
                                    icons = [surface_manager.add_icon('club', ':mace.png')],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'simple weapon'],
                                    rarity = 'common',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(3, 'crushing')],
                                            critical_range = 11,
                                            critical_damage = 3,
                                            weapon_class = 'simple')))

    config.append(
                  ItemConfiguration(name = 'warhammer',
                                    cost = 6,
                                    weight = 4,
                                    icons = [surface_manager.add_icon('warhammer', ':gavel.png')],
                                    types = ['weapon',
                                             'two-handed',
                                             'melee',
                                             'martial weapon'],
                                    rarity = 'rare',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(7, 'crushing')],
                                            critical_range = 12,
                                            critical_damage = 7,
                                            weapon_class = 'martial')))

    config.append(
                  ItemConfiguration(name = 'spear',
                                    cost = 6,
                                    weight = 4,
                                    icons = [surface_manager.add_icon('spear', ':barbed-spear.png')],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'martial weapon'],
                                    rarity = 'rare',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(5, 'piercing')],
                                            critical_range = 11,
                                            critical_damage = 5,
                                            weapon_class = 'martial')))

    config.append(
                  ItemConfiguration(name = 'whip',
                                    cost = 6,
                                    weight = 4,
                                    icons = [surface_manager.add_icon('whip', ':whip.png')],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'exotic weapon'],
                                    rarity = 'common',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(3, 'slashing')],
                                            critical_range = 11,
                                            critical_damage = 3,
                                            weapon_class = 'exotic')))

    config.append(
                  ItemConfiguration(name = 'sickle',
                                    cost = 6,
                                    weight = 4,
                                    icons = [surface_manager.add_icon('sickle', ':scythe.png')],
                                    types = ['weapon',
                                             'light weapon',
                                             'melee',
                                             'exotic weapon'],
                                    rarity = 'common',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(3, 'slashing')],
                                            critical_range = 10,
                                            critical_damage = 3,
                                            weapon_class = 'exotic')))

    config.append(
                  ItemConfiguration(name = 'morning star',
                                    cost = 6,
                                    weight = 4,
                                    icons = [surface_manager.add_icon('morning star', ':spiked-mace.png')],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'martial weapon'],
                                    rarity = 'uncommon',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(2, 'crushing'),
                                                      (2, 'piercing')],
                                            critical_range = 12,
                                            critical_damage = 2,
                                            weapon_class = 'martial')))

    config.append(
                  ItemConfiguration(name = 'robes',
                                    cost = 2,
                                    weight = 4,
                                    icons = [surface_manager.add_icon('robes', ':robes.png')],
                                    types = ['armour'],
                                    rarity = 'common',
                                    armour_configuration = ArmourConfiguration(
                                                damage_reduction = 0,
                                                speed_modifier = 1.0)))
    config.append(
                  ItemConfiguration(name = 'leather armour',
                                    cost = 4,
                                    weight = 6,
                                    icons = [surface_manager.add_icon('leather armour', ':leather_armour.png')],
                                    types = ['armour'],
                                    rarity = 'common',
                                    armour_configuration = ArmourConfiguration(
                                                damage_reduction = 1,
                                                speed_modifier = 1.0)))
    config.append(
                  ItemConfiguration(name = 'chainmail',
                                    cost = 8,
                                    weight = 12,
                                    icons = [surface_manager.add_icon('chainmail', ':chainmail.png')],
                                    types = ['armour'],
                                    rarity = 'uncommon',
                                    armour_configuration = ArmourConfiguration(
                                                damage_reduction = 2,
                                                speed_modifier = 0.9)))
    config.append(
                  ItemConfiguration(name = 'scale mail',
                                    cost = 12,
                                    weight = 12,
                                    icons = [surface_manager.add_icon('scale mail', ':scale_mail.png')],
                                    types = ['armour'],
                                    rarity = 'uncommon',
                                    armour_configuration = ArmourConfiguration(
                                                damage_reduction = 3,
                                                speed_modifier = 0.7)))
    config.append(
                  ItemConfiguration(name = 'plate mail',
                                    cost = 2,
                                    weight = 4,
                                    icons = [surface_manager.add_icon('plate mail', ':plate_mail.png')],
                                    types = ['armour'],
                                    rarity = 'rare',
                                    armour_configuration = ArmourConfiguration(
                                                damage_reduction = 5,
                                                speed_modifier = 0.5)))
    config.append(
                  ItemConfiguration(name = 'healing potion',
                                    cost = 150,
                                    weight = 1,
                                    icons = [surface_manager.add_icon('plain_potion', ':plain_potion.png')],
                                    types = ['potion'],
                                    rarity = 'rare',
                                    effect_handles = [EffectHandle(
                                            trigger = 'on drink',
                                            effect = 'cure medium wounds',
                                            parameters = None,
                                            charges = 1)]))

    return config

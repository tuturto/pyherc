# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
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
module for configuring catacombs
"""
from pyherc.data.effects import EffectHandle, MovementModeModifier
from pyherc.generators import (AmmunitionConfiguration, ArmourConfiguration,
                               ItemConfiguration, WeaponConfiguration, TrapConfiguration,
                               BootsConfiguration)
from pyherc.rules.constants import (CRUSHING_DAMAGE, PIERCING_DAMAGE,
                                    SLASHING_DAMAGE)


def init_items(context):
    """
    Initialise common items

    :returns: item configurations
    :rtype: [ItemConfiguration]
    """
    surface_manager = context.surface_manager
    config = []

    config.append(ItemConfiguration(name = 'dagger',
                                    description = 'Light and simple weapon that does not do much damage. Small size allows skilled wielder to do critical damage easily though.',
                                    cost = 10,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'dagger',
                                                            ':dagger.png',
                                                            ')',
                                                            ['dim', 'cyan'])],
                                    types = ['weapon',
                                             'light weapon',
                                             'melee',
                                             'simple weapon'],
                                    rarity = 'common',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(2, PIERCING_DAMAGE)],
                                            critical_range = 10,
                                            critical_damage = 2,
                                            weapon_class = 'simple',
                                            speed = 1.5)))

    config.append(ItemConfiguration(name = 'sword',
                                    description = 'Staple tool for adventurers and soldiers alike. Swords do more damage than daggers, but are harder to use effectively.',
                                    cost = 20,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'sword',
                                                            ':stiletto.png',
                                                            ')',
                                                            ['dim', 'cyan'])],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'martial weapon'],
                                    rarity = 'uncommon',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(2, PIERCING_DAMAGE),
                                                      (2, SLASHING_DAMAGE)],
                                            critical_range = 12,
                                            critical_damage = 2,
                                            weapon_class = 'martial',
                                            speed = 1.0)))

    config.append(ItemConfiguration(name = 'axe',
                                    description = 'Heavy battle axes can cut through flesh and crush through bones. Not very common weapon, because effective use requires years of training.',
                                    cost = 20,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'axe',
                                                            ':battle-axe.png',
                                                            ')',
                                                            ['dim', 'cyan'])],
                                    types = ['weapon',
                                             'two-handed',
                                             'melee',
                                             'martial weapon'],
                                    rarity = 'uncommon',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(2, CRUSHING_DAMAGE),
                                                      (2, SLASHING_DAMAGE)],
                                            critical_range = 12,
                                            critical_damage = 2,
                                            weapon_class = 'martial',
                                            speed = 1.0)))

    config.append(ItemConfiguration(name = 'club',
                                    description = 'Simple and easy to use weapon, that can be used effectively with one hand.',
                                    cost = 6,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'club',
                                                            ':mace.png',
                                                            ')',
                                                            ['dim', 'cyan'])],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'simple weapon'],
                                    rarity = 'common',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(3, CRUSHING_DAMAGE)],
                                            critical_range = 11,
                                            critical_damage = 3,
                                            weapon_class = 'simple',
                                            speed = 0.8)))

    config.append(ItemConfiguration(name = 'warhammer',
                                    description = 'Heavy two-handed weapon that crushes through but the strongest defences. Rare sight in the battle field, because of the huge weight.',
                                    cost = 50,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'warhammer',
                                                            ':gavel.png',
                                                            ')',
                                                            ['dim', 'cyan'])],
                                    types = ['weapon',
                                             'two-handed',
                                             'melee',
                                             'martial weapon'],
                                    rarity = 'rare',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(7, CRUSHING_DAMAGE)],
                                            critical_range = 12,
                                            critical_damage = 7,
                                            weapon_class = 'martial',
                                            speed = 0.5)))

    config.append(ItemConfiguration(name = 'spear',
                                    description = 'One handed piercing weapon that can be devastating in hands of skilled user.',
                                    cost = 25,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'spear',
                                                            ':barbed-spear.png',
                                                            ')',
                                                            ['dim', 'cyan'])],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'martial weapon'],
                                    rarity = 'rare',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(5, PIERCING_DAMAGE)],
                                            critical_range = 11,
                                            critical_damage = 5,
                                            weapon_class = 'martial',
                                            speed = 0.6)))

    config.append(ItemConfiguration(name = 'whip',
                                    description = 'Weapon of choice for archeologists and vampire hunters. Not particularly strong, but very versatile.',
                                    cost = 25,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'whip',
                                                            ':whip.png',
                                                            ')',
                                                            ['dim', 'yellow'])],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'exotic weapon'],
                                    rarity = 'common',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(3, SLASHING_DAMAGE)],
                                            critical_range = 11,
                                            critical_damage = 3,
                                            weapon_class = 'exotic',
                                            speed = 0.8)))

    config.append(ItemConfiguration(name = 'sickle',
                                    description = 'Farming implement repurposed on the battle field. Light and common weapon that requires very specifically trained user.',
                                    cost = 6,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'sickle',
                                                            ':scythe.png',
                                                            ')',
                                                            ['dim', 'cyan'])],
                                    types = ['weapon',
                                             'light weapon',
                                             'melee',
                                             'exotic weapon'],
                                    rarity = 'common',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(3, SLASHING_DAMAGE)],
                                            critical_range = 10,
                                            critical_damage = 3,
                                            weapon_class = 'exotic',
                                            speed = 1.2)))

    config.append(ItemConfiguration(name = 'morning star',
                                    description = 'Spiked club, guaranteed to pierce through armours and crush through bones. Difficult to use weapon that requires years of practice.',
                                    cost = 40,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'morning star',
                                                            ':spiked-mace.png',
                                                            ')',
                                                            ['dim', 'cyan'])],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'martial weapon'],
                                    rarity = 'uncommon',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(2, CRUSHING_DAMAGE),
                                                      (2, PIERCING_DAMAGE)],
                                            critical_range = 12,
                                            critical_damage = 2,
                                            weapon_class = 'martial',
                                            speed = 1.0)))

    config.append(ItemConfiguration(name = 'bow',
                                    description = 'Short bow, built from laminated bones and wood. Perfect for ranged combat.',
                                    cost = 10,
                                    weight = 3,
                                    icons = [surface_manager.add_icon(
                                                            'bow',
                                                            ':bow.png',
                                                            ')',
                                                            ['dim', 'yellow'])],
                                    types = ['weapon',
                                             'two-handed',
                                             'ranged',
                                             'martial weapon'],
                                    rarity = 'uncommon',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(1, CRUSHING_DAMAGE)],
                                            critical_range = 12,
                                            critical_damage = 1,
                                            weapon_class = 'martial',
                                            ammunition_type = 'arrow',
                                            speed = 1.0)))

    config.append(ItemConfiguration(name = 'arrow',
                                    description = 'Wooden arrows tipped with metal head.',
                                    cost = 1,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'arrows',
                                                            ':arrows.png',
                                                            ')',
                                                            ['dim', 'yellow'])],
                                    types = ['ammunition'],
                                    rarity = 'uncommon',
                                    ammunition_configuration = AmmunitionConfiguration(
                                            damage = [(3, PIERCING_DAMAGE)],
                                            critical_range = 12,
                                            critical_damage = 3,
                                            ammunition_type = 'arrow',
                                            count = 15)))

    config.append(ItemConfiguration(name = 'war arrow',
                                    description = 'Wooden arrows tipped with metal head that have cutting edge.',
                                    cost = 1,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'arrows',
                                                            ':arrows.png',
                                                            ')',
                                                            ['dim', 'yellow'])],
                                    types = ['ammunition'],
                                    rarity = 'uncommon',
                                    ammunition_configuration = AmmunitionConfiguration(
                                            damage = [(1, PIERCING_DAMAGE),
                                                      (2, SLASHING_DAMAGE)],
                                            critical_range = 12,
                                            critical_damage = 3,
                                            ammunition_type = 'arrow',
                                            count = 15)))

    config.append(ItemConfiguration(name = 'blunt arrow',
                                    description = 'Wooden arrows with wide end, used to cause blunt trauma.',
                                    cost = 1,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'arrows',
                                                            ':arrows.png',
                                                            ')',
                                                            ['dim', 'yellow'])],
                                    types = ['ammunition'],
                                    rarity = 'uncommon',
                                    ammunition_configuration = AmmunitionConfiguration(
                                            damage = [(3, CRUSHING_DAMAGE)],
                                            critical_range = 12,
                                            critical_damage = 3,
                                            ammunition_type = 'arrow',
                                            count = 15)))

    config.append(ItemConfiguration(name = 'spade',
                                    description = 'Simple, but effective tool for digging holes.',
                                    cost = 5,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'spade',
                                                            ':spade.png',
                                                            '(',
                                                            ['dim', 'cyan'])],
                                    types = ['weapon',
                                             'melee',
                                             'simple weapon',
                                             'spade'],
                                    rarity = 'common',
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(1, CRUSHING_DAMAGE)],
                                            critical_range = 12,
                                            critical_damage = 1,
                                            weapon_class = 'simple',
                                            speed = 0.9)))


    config.append(ItemConfiguration(name = 'robes',
                                    description = 'Simple robes are favoured by spell casters. They do not hinder magical abilities and strong wizards are more than capable of deflecting attacks anyway.',
                                    cost = 5,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'robes',
                                                            ':robes.png',
                                                            '[',
                                                            ['dim', 'yellow'])],
                                    types = ['armour'],
                                    rarity = 'common',
                                    armour_configuration = ArmourConfiguration(
                                                damage_reduction = 0,
                                                speed_modifier = 1.0)))

    config.append(ItemConfiguration(name = 'leather armour',
                                    description = 'Armour made of hardened leather. While it offers only meager protection, it allows the wearer to move very swiftly.',
                                    cost = 10,
                                    weight = 6,
                                    icons = [surface_manager.add_icon(
                                                            'leather armour',
                                                            ':leather_armour.png',
                                                            '[',
                                                            ['dim', 'yellow'])],
                                    types = ['armour'],
                                    rarity = 'common',
                                    armour_configuration = ArmourConfiguration(
                                                damage_reduction = 1,
                                                speed_modifier = 1.0)))

    config.append(ItemConfiguration(name = 'chainmail',
                                    description = 'Armour made of countless interlocking metal rings. Somewhat heavier than leather armour.',
                                    cost = 20,
                                    weight = 12,
                                    icons = [surface_manager.add_icon(
                                                            'chainmail',
                                                            ':chainmail.png',
                                                            '[',
                                                            ['dim', 'cyan'])],
                                    types = ['armour'],
                                    rarity = 'uncommon',
                                    armour_configuration = ArmourConfiguration(
                                                damage_reduction = 2,
                                                speed_modifier = 0.9)))

    config.append(ItemConfiguration(name = 'scale mail',
                                    description = 'Scale mail is made of interlocking scales, in a similar manner to chainmail. It offers better protection, while being heavier and harder to move around with.',
                                    cost = 25,
                                    weight = 12,
                                    icons = [surface_manager.add_icon(
                                                            'scale mail',
                                                            ':scale_mail.png',
                                                            '[',
                                                            ['dim', 'cyan'])],
                                    types = ['armour'],
                                    rarity = 'uncommon',
                                    armour_configuration = ArmourConfiguration(
                                                damage_reduction = 3,
                                                speed_modifier = 0.7)))

    config.append(ItemConfiguration(name = 'plate mail',
                                    description = 'Ultimate solution for protection. Heavy plates cover wearer from head to toe, offering great protection against attacks.',
                                    cost = 50,
                                    weight = 4,
                                    icons = [surface_manager.add_icon(
                                                            'plate mail',
                                                            ':plate_mail.png',
                                                            '[',
                                                            ['dim', 'cyan'])],
                                    types = ['armour'],
                                    rarity = 'rare',
                                    armour_configuration = ArmourConfiguration(
                                                damage_reduction = 5,
                                                speed_modifier = 0.5)))

    config.append(ItemConfiguration(name = 'leather shoes',
                                    description = 'Simple shoes for those wishing to travel light.',
                                    cost = 5,
                                    weight = 1,
                                    icons = [surface_manager.add_icon('leather_shoes',
                                                                      ':items/boots_1.png',
                                                                      '[',
                                                                      ['dim', 'yellow'])],
                                    types = ['boots'],
                                    rarity = 'common',
                                    boots_configuration = BootsConfiguration(
                                        damage_reduction = 0,
                                        speed_modifier = 1)))

    config.append(ItemConfiguration(name = 'heavy boots',
                                    description = 'Rather heavy boots, which will protect you.',
                                    cost = 5,
                                    weight = 1,
                                    icons = [surface_manager.add_icon('heavy_boots',
                                                                      ':items/boots_3.png',
                                                                      '[',
                                                                      ['dim', 'yellow'])],
                                    types = ['boots'],
                                    rarity = 'uncommon',
                                    boots_configuration = BootsConfiguration(
                                        damage_reduction = 1,
                                        speed_modifier = 0.8)))

    config.append(ItemConfiguration(name = 'air shoes',
                                    description = 'Clunky metal shoes that lift you in air.',
                                    cost = 5,
                                    weight = 1,
                                    icons = [surface_manager.add_icon('mechanical_shoes',
                                                                      ':items/boots_2.png',
                                                                      '[',
                                                                      ['dim', 'yellow'])],
                                    types = ['boots'],
                                    rarity = 'rare',
                                    boots_configuration = BootsConfiguration(
                                        damage_reduction = 0,
                                        speed_modifier = 0.7),
                                    effects = [MovementModeModifier(duration = None,
                                                                    frequency = None,
                                                                    tick = None,
                                                                    icon = None,
                                                                    title = "fly boosters",
                                                                    description = "fly boosters",
                                                                    mode = "fly")]))

    config.append(ItemConfiguration(name = 'speed shoes',
                                    description = 'Very light weight shoes, perfect for running.',
                                    cost = 5,
                                    weight = 1,
                                    icons = [surface_manager.add_icon('speed_shoes',
                                                                      ':items/boots_1.png',
                                                                      '[',
                                                                      ['dim', 'yellow'])],
                                    types = ['boots'],
                                    rarity = 'rare',
                                    boots_configuration = BootsConfiguration(
                                        damage_reduction = -2,
                                        speed_modifier = 1.3)))

    config.append(ItemConfiguration(name = 'healing potion',
                                    cost = 150,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'plain_potion',
                                                            ':plain_potion.png',
                                                            '!',
                                                            ['red'])],
                                    types = ['potion'],
                                    rarity = 'rare',
                                    effect_handles = [EffectHandle(
                                            trigger = 'on drink',
                                            effect = 'cure medium wounds',
                                            parameters = None,
                                            charges = 1)]))

    config.append(ItemConfiguration(name = 'idol of snowman',
                                    description = 'An idol of snowman, walking in the air',
                                    cost = 0,
                                    weight = 0,
                                    icons = [surface_manager.add_icon(
                                                            'snowman',
                                                            ':snowman.png',
                                                            '`',
                                                            ['dim', 'white'])],
                                    types = ['event item', 'idol'],
                                    rarity = 'artifact'))

    return config

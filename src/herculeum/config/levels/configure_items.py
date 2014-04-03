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
module for configuring catacombs
"""
from pyherc.data.effects import EffectHandle
from pyherc.generators import (AmmunitionConfiguration, ArmourConfiguration,
                               ItemConfiguration, WeaponConfiguration)
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

    config.append(ItemConfiguration(name = 'apple',
                                    cost = 1,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'apple',
                                                            ':apple.png',
                                                            '%',
                                                            ['red'])],
                                    types = ['food'],
                                    rarity = 'common'))

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

    config.append(ItemConfiguration(name = 'Tome of Um\'bano - Page 150',
                                    description = 'In crypt under Herculeum, I encountered giant spiders. These arachnids have poisoned bite and could easily take down unprepared adventurer. Dealing with them from distance seems to be the best approach, if cramped surroundings just allow for it.',
                                    cost = 100,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'tied-scroll',
                                                            ':tied-scroll.png',
                                                            '?',
                                                            ['dim', 'yellow'])],
                                    types = ['tome'],
                                    rarity = 'rare'))

    config.append(ItemConfiguration(name = 'Tome of Um\'bano - Page 158',
                                    description = 'Patrolling skeleton warriors have been easy to avoid so far. They patrol mindlessly around the catacombs and only turn to pursue if I approach too close. They lose interest soon after I retreat and return to their endless patrol.',
                                    cost = 100,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'tied-scroll',
                                                            ':tied-scroll.png',
                                                            '?',
                                                            ['dim', 'yellow'])],
                                    types = ['tome'],
                                    rarity = 'rare'))

    config.append(ItemConfiguration(name = 'Tome of Um\'bano - Page 326',
                                    description = 'In the ancient times, old evil ruled over the land and terrorized everything. Kingdoms were drowned in fire and destroyed by demon, Crimson Jaw. Only when seven sages combined their powers, they could overcome him. But Crimson Jaw was too strong to be destroyed completely and his spirit had to be bound and trapped. Crimson Lair is his final resting place, where seals of seven sages keep him imprisoned.',
                                    cost = 100,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'tied-scroll',
                                                            ':tied-scroll.png',
                                                            '?',
                                                            ['dim', 'yellow'])],
                                    types = ['tome'],
                                    rarity = 'rare'))

    config.append(ItemConfiguration(name = 'Tome of Um\'bano - Page 485',
                                    description = 'The whip of Ashmque is a horrendous weapon. Thong of the whip is made of blackened links of steel and an eternal flame is burning around it. Only the strongest of men can even try to wield it because of the heavy construction. It is said that the whip of Ashmque was forged at the dawn of ages by demon smith Ashmque.',
                                    cost = 100,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'tied-scroll',
                                                            ':tied-scroll.png',
                                                            '?',
                                                            ['dim', 'yellow'])],
                                    types = ['tome'],
                                    rarity = 'rare'))

    config.append(ItemConfiguration(name = 'Tome of Um\'bano - Page 612',
                                    description = 'Prince Razel was obsessed with alchemy and built a complex laboratory under city of Herculeum. Untold experiments were conducted there and it is rumoured that those experiments ultimately caused his death.',
                                    cost = 100,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'tied-scroll',
                                                            ':tied-scroll.png',
                                                            '?',
                                                            ['dim', 'yellow'])],
                                    types = ['tome'],
                                    rarity = 'rare'))

    config.append(ItemConfiguration(name = 'Tome of Um\'bano - Page 615',
                                    description = 'Tomb of Prince Razel is rumoured to have been filled with traps and experiments he conducted while he was still living. The exact location of the tomb has been lost in the mists of time, but I think it has to be near his hidden laboratory.',
                                    cost = 100,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'tied-scroll',
                                                            ':tied-scroll.png',
                                                            '?',
                                                            ['dim', 'yellow'])],
                                    types = ['tome'],
                                    rarity = 'rare'))

    config.append(ItemConfiguration(name = 'Tome of Um\'bano - Page 621',
                                    description = 'Prince Razel\'s greatest experiment was a staff that could shoot fire on command. He never revealed how he created it and guarded the staff jealously.',
                                    cost = 100,
                                    weight = 1,
                                    icons = [surface_manager.add_icon(
                                                            'tied-scroll',
                                                            ':tied-scroll.png',
                                                            '?',
                                                            ['dim', 'yellow'])],
                                    types = ['tome'],
                                    rarity = 'rare'))

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

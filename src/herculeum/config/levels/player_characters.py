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
module for configuring player characters
"""
import datetime

from pyherc.data import SpecialTime
from pyherc.generators import creature_config, inventory_config
from pyherc.rules.calendar import get_special_events


def init_players(context):
    """
    Initialise creatures

    :returns: list of creature configurations
    :rtype: [CreatureConfiguration]
    """
    config = []
    surface_manager = context.surface_manager

    adventurer_f0 = surface_manager.add_icon('adventurer_f0', ':pc_adventurer_f0.png', '@', ['white', 'bold'])
    adventurer_f1 = surface_manager.add_icon('adventurer_f1', ':pc_adventurer_f1.png', '@', ['white', 'bold'])
    config.append(creature_config(name = 'Adventurer',
                                  body = 6,
                                  finesse = 7,
                                  mind = 8,
                                  hp = 9,
                                  speed = 2.5,
                                  icons = (adventurer_f0, adventurer_f1),
                                  attack = 1,
                                  ai = None,
                                  effect_handles = None,
                                  inventory = [inventory_config(
                                      item_name = 'sword',
                                      min_amount = 1,
                                      max_amount = 1,
                                      probability = 100),
                                               inventory_config(
                                                   item_name = 'leather armour',
                                                   min_amount = 1,
                                                   max_amount = 1,
                                                   probability = 100),
                                               inventory_config(
                                                   item_name = 'bow',
                                                   min_amount = 1,
                                                   max_amount = 1,
                                                   probability = 100),
                                               inventory_config(
                                                   item_name = 'arrow',
                                                   min_amount = 1,
                                                   max_amount = 1,
                                                   probability = 100),
                                               inventory_config(
                                                   item_name = 'war arrow',
                                                   min_amount = 1,
                                                   max_amount = 1,
                                                   probability = 100),
                                               inventory_config(
                                                   item_name = 'blunt arrow',
                                                   min_amount = 1,
                                                   max_amount = 1,
                                                   probability = 100),
                                               inventory_config(
                                                   item_name = 'healing potion',
                                                   min_amount = 1,
                                                   max_amount = 2,
                                                   probability = 50)],
                                  description = '\n'.join(['A skillful adventurer.',
                                                           '',
                                                           'Adventurer is armed and ready to explore any dungeon he sees. He is strong enough to survive combat with some of the dangers, while some he definitely should avoid',
                                                           'Adventurer also carries some potions that will help him on his journey.'])))

    warrior_f0 = surface_manager.add_icon('warrior_f0', ':pc_warrior_f0.png', '@', ['white', 'bold'])
    warrior_f1 = surface_manager.add_icon('warrior_f1', ':pc_warrior_f1.png', '@', ['white', 'bold'])
    config.append(creature_config(name = 'Warrior',
                                  body = 8,
                                  finesse = 7,
                                  mind = 6,
                                  hp = 12,
                                  speed = 2.5,
                                  icons = (warrior_f0, warrior_f1),
                                  attack = 2,
                                  ai = None,
                                  effect_handles = None,
                                  inventory = [inventory_config(
                                      item_name = 'sword',
                                      min_amount = 1,
                                      max_amount = 1,
                                      probability = 100),
                                               inventory_config(
                                                   item_name = 'warhammer',
                                                   min_amount = 1,
                                                   max_amount = 1,
                                                   probability = 100),
                                               inventory_config(
                                                   item_name = 'scale mail',
                                                   min_amount = 1,
                                                   max_amount = 1,
                                                   probability = 100),
                                               inventory_config(
                                                   item_name = 'dagger',
                                                   min_amount = 1,
                                                   max_amount = 1,
                                                   probability = 100)],
                                  description = '\n'.join(['A stout warrior',
                                                                '',
                                                                'Warrior is armed to teeth and tends to solve his problems with brute force.',
                                                                'Warrior has nice selection of weapons to use but very little of anything else.'])))

    mage_f0 = surface_manager.add_icon('mage_f0', ':pc_mage_f0.png', '@', ['white', 'bold'])
    mage_f1 = surface_manager.add_icon('mage_f1', ':pc_mage_f1.png', '@', ['white', 'bold'])
    config.append(creature_config(name = 'Mage',
                                  body = 3,
                                  finesse = 5,
                                  mind = 11,
                                  hp = 6,
                                  speed = 2.5,
                                  icons = (mage_f0, mage_f1),
                                  attack = 1,
                                  ai = None,
                                  effect_handles = None,
                                  inventory = [inventory_config(
                                      item_name = 'dagger',
                                      min_amount = 1,
                                      max_amount = 1,
                                      probability = 100),
                                               inventory_config(
                                                   item_name = 'robes',
                                                   min_amount = 1,
                                                   max_amount = 1,
                                                   probability = 100),
                                               inventory_config(
                                                   item_name = 'healing potion',
                                                   min_amount = 1,
                                                   max_amount = 2,
                                                   probability = 50)],
                                        description = '\n'.join(['A wise mage.',
                                                                '',
                                                                'A mage is physically weak and mentally strong. He should avoid combat at all cost and deal with the enemies by using his spells.',
                                                                'Mage also carries some potions that will help him on his journey.'])))

    date = datetime.date.today()
    events = get_special_events(date.year, date.month, date.day)

    if SpecialTime.aprilfools in events:

        platino_f0 = surface_manager.add_icon('platino_f0', ':platino_f0.png', '@', ['white', 'bold'])
        platino_f1 = surface_manager.add_icon('platino_f1', ':platino_f1.png', '@', ['white', 'bold'])
        config.append(creature_config(name = 'Dragon de Platino',
                                      body = 6,
                                      finesse = 7,
                                      mind = 8,
                                      hp = 9,
                                      speed = 2.5,
                                      icons = (platino_f0, platino_f1),
                                      attack = 1,
                                      ai = None,
                                      effect_handles = None,
                                      inventory = [],
                                      description = '\n'.join(['Dragon de Platino',
                                                               '',
                                                               'Mysterious dragon who comes and goes as he wishes...'])))

    if SpecialTime.christmas in events:
        for character in config:
            character.inventory.append(inventory_config(item_name = 'idol of snowman',
                                                              min_amount = 1,
                                                              max_amount = 1,
                                                              probability = 100))

    return config

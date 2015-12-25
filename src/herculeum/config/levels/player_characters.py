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
                                  hp = 12,
                                  speed = 2.5,
                                  icons = (adventurer_f0, adventurer_f1),
                                  attack = 1,
                                  ai = None,
                                  effect_handles = None,
                                  inventory = [inventory_config(
                                      item_name = 'spade',
                                      min_amount = 1,
                                      max_amount = 1,
                                      probability = 100),
                                               inventory_config(
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
                                                   probability = 50),
                                               inventory_config(
                                                   item_name = 'bag of small caltrops',
                                                   min_amount = 1,
                                                   max_amount = 1,
                                                   probability = 20)],
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
                                  hp = 16,
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

    surface_manager.add_icon('engineer_f0', ':/characters/pc_engineer_f0.png', '@', ['white', 'bold'])
    surface_manager.add_icon('engineer_f1', ':/characters/pc_engineer_f1.png', '@', ['white', 'bold'])
    config.append(creature_config(name = 'Master Engineer',
                                  body = 3,
                                  finesse = 5,
                                  mind = 11,
                                  hp = 8,
                                  speed = 2.5,
                                  icons = ('engineer_f0', 'engineer_f1'),
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
                                                   probability = 50),
                                               inventory_config(
                                                   item_name = 'bag of brutal caltrops',
                                                   min_amount = 1,
                                                   max_amount = 2,
                                                   probability = 100),
                                               inventory_config(
                                                   item_name = 'greater bag of caltrops',
                                                   min_amount = 1,
                                                   max_amount = 2,
                                                   probability = 100)],
                                  description = '\n'.join(['A master engineer.',
                                                           '',
                                                                'Master engineer is physically weak and should avoid direct combat with enemies. Their skill lies in various tools and gadgets that can be used to defeat the foes.',
                                                           'Master engineer also carries some potions that are useful while exploring dungeons.'])))

    date = datetime.date.today()
    events = get_special_events(date.year, date.month, date.day)

    if False and SpecialTime.aprilfools in events:

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

    if False and SpecialTime.christmas in events:
        for character in config:
            character.inventory.append(inventory_config(item_name = 'idol of snowman',
                                                        min_amount = 1,
                                                        max_amount = 1,
                                                        probability = 100))

    return config

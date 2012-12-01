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
Module for creature generation related classes
"""
from pyherc.data import Character, Inventory
from pyherc.data.effects import EffectHandle, EffectsCollection
from pyherc.aspects import logged

class CreatureGenerator(object):
    """
    Class used to generate creatures
    """
    @logged
    def __init__(self, configuration, model, item_generator, rng):
        """
        Default constructor
        """
        super(CreatureGenerator, self).__init__()
        self.configuration = configuration
        self.model = model
        self.rng = rng
        self.item_generator = item_generator

    @logged
    def generate_creature(self, name):
        """
        Generate creature

        :param name: name of the creature to generate
        :type name: string
        """
        config = self.__get_creature_config(name)

        new_creature = Character(self.model,
                                 EffectsCollection(),
                                 Inventory())

        new_creature.name = config.name
        new_creature.body = config.body
        new_creature.finesse = config.finesse
        new_creature.mind = config.mind
        new_creature.hit_points = config.hp
        new_creature.max_hp = config.hp
        new_creature.speed = config.speed
        new_creature.icon = config.icons #TODO: pick random
        new_creature.attack = config.attack

        for spec in config.effect_handles:
            new_handle = EffectHandle(trigger = spec.trigger,
                                       effect = spec.effect,
                                       parameters = spec.parameters,
                                       charges = spec.charges)

            new_creature.add_effect_handle(new_handle)

        for spec in config.effects:
            #TODO: temporary hack for techday demo
            new_effect = spec.clone()
            new_creature.add_effect(new_effect)


        for spec in config.inventory:
            new_creature.inventory.append(
                                self.item_generator.generate_item(
                                                        name = spec.item_name))

        if not config.ai == None:
            new_creature.artificial_intelligence = config.ai(new_creature)

        return new_creature

    @logged
    def __get_creature_config(self, name):
        """
        Get creature config

        :param name: name of the creature
        :type name: string
        """
        return self.configuration[name]

class CreatureConfiguration(object):
    """
    Configuration for an creature
    """

    def __init__(self, name, body, finesse, mind, hp, speed, icons, attack,
                 ai = None, effect_handles = None, effects = None,
                 inventory = None, description = None):
        """
        Default constructor
        """
        self.name = name
        self.body = body
        self.finesse = finesse
        self.mind = mind
        self.hp = hp
        self.speed = speed
        self.icons = icons
        self.attack = attack
        self.ai = ai
        self.description = description

        if effect_handles == None:
            self.effect_handles = []
        else:
            self.effect_handles = effect_handles

        if effects == None:
            self.effects = []
        else:
            self.effects = effects

        if inventory == None:
            self.inventory = []
        else:
            self.inventory = inventory

class InventoryConfiguration(object):
    """
    Configuration for inventory of a creature

    .. versionadded:: 0.6
    """
    def __init__(self, item_name, min_amount, max_amount, probability):
        """
        Default constructor
        """
        self.item_name = item_name
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.probability = probability

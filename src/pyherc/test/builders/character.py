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
Module for character builder
"""
from pyherc.data import Character, Inventory
from pyherc.data.effects import EffectsCollection
from mockito import mock

class CharacterBuilder(object):
    """
    Class for building Characters
    """
    def __init__(self):
        """
        Default constructor
        """
        super(CharacterBuilder, self).__init__()
        self.hit_points = 10
        self.max_hp = 10
        self.model = mock()

        self.speed = 1
        self.tick = 0
        self.attack = 1
        self.body = 1
        self.mind = 1
        self.finesse = 1

        self.name = 'prototype'

        self.level = None
        self.location = ()

        self.items = []

        self.effect_handles = []
        self.effects = []
        self.effects_collection = EffectsCollection()
        self.inventory = Inventory()
        self.player_character = False

        self.listeners = []
        self.update_listeners = []

    def as_player_character(self):
        """
        Configure generated character to be player
        """
        self.player_character = True
        return self

    def with_model(self, model):
        """
        Use given model

        :param model: model
        :type model: Model
        """
        self.model = model
        return self

    def with_effect_handle(self, handle):
        """
        Add effect handle to generated character

        :param handle: effect handle
        :type handle: EffectHandle
        """
        if hasattr(handle, 'build'):
            self.effect_handles.append(handle.build())
        else:
            self.effect_handles.append(handle)
        return self

    def with_effect(self, effect):
        """
        Add effect to generated character

        :param effect: effect
        :type effect: Effect
        """
        if hasattr(effect, 'build'):
            self.effects.append(effect.build())
        else:
            self.effects.append(effect)
        return self

    def with_hit_points(self, hit_points):
        """
        Configure amount of hit points

        :param hit_points: hit points
        :type hit_points: int
        """
        self.hit_points = hit_points
        return self

    def with_max_hp(self, max_hp):
        """
        Configure maximum amount of hit points

        :param max_hp: maximum hit points
        :type max_hp: int
        """
        self.max_hp = max_hp
        return self

    def with_speed(self, speed):
        """
        Configure speed

        :param speed: speed of character
        :type speed: int
        """
        self.speed = speed
        return self

    def with_mind(self, mind):
        """
        Configure mind

        :param mind: mind of character
        :type mind: int
        """
        self.mind = mind
        return self

    def with_tick(self, tick):
        """
        Set internal clock of character

        :param tick: tick
        :type tick: int
        """
        self.tick = tick
        return self

    def with_attack(self, attack):
        """
        Configure attack value of character

        :param attack: attack value
        :type attack: int
        """
        self.attack = attack
        return self

    def with_body(self, body):
        """
        Configure body value of character

        :param body: body value
        :type body: int
        """
        self.body = body
        return self

    def with_level(self, level):
        """
        Set level where character is located

        :param level: level
        :type level: Level
        """
        self.level = level
        return self

    def with_location(self, location):
        """
        Set location of character

        :param location: location
        :type location: (int, int)
        """
        self.location = location
        return self

    def with_name(self, name):
        """
        Set name of character

        :param name: name
        :type name: string
        """
        self.name = name
        return self

    def with_event_listener(self, listener):
        """
        Register event listener to listen this character

        :param listener: listener
        :type listener: listener

        .. note:: Can be called multiple times
        """
        self.listeners.append(listener)
        return self

    def with_update_listener(self, listener):
        """
        Register update listener to listen this character

        :param listener: listener
        :type listener: listner

        .. note:: Can be called multiple times
        """
        self.update_listeners.append(listener)
        return self

    def with_item(self, item):
        """
        Add item into characters inventory

        :param item: item to add
        :type item: Item

        .. note:: Can be called multiple times
        """
        if hasattr(item, 'build'):
            self.items.append(item.build())
        else:
            self.items.append(item)

        return self

    def with_finesse(self, finesse):
        """
        Set finesse of the character

        :param finesse: finesse to set
        :type finesse: integer
        """
        self.finesse = finesse
        return self

    def build(self):
        """
        Build character

        :returns: character
        :rtype: Character
        """
        character = Character(model = self.model,
                              effects_collection = self.effects_collection,
                              inventory = self.inventory)

        if self.player_character:
            self.model.player = character

        character.name = self.name

        character.hit_points = self.hit_points
        character.max_hp = self.max_hp

        character.mind = self.mind
        character.body = self.body
        character.finesse = self.finesse
        character.attack = self.attack

        character.speed = self.speed
        character.tick = self.tick
        character.level = self.level
        character.location = self.location

        for item in self.items:
            character.inventory.append(item)

        for handle in self.effect_handles:
            character.add_effect_handle(handle)

        for effect in self.effects:
            character.add_effect(effect)

        for listener in self.listeners:
            character.register_event_listener(listener)

        for listener in self.update_listeners:
            character.register_for_updates(listener)

        return character

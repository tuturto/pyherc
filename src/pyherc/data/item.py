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
Module for item related classes

Classes:
    Item
    WeaponData
"""
from pyherc.aspects import Logged

class Item(object):
    """
    Represents item
    """
    logged = Logged()

    def __init__(self, effects_collection):
        """
        Default constructor

        :param effects_collection: collection for effects
        :type effects_collection: EffectsCollection
        """
        super(Item, self).__init__()
        #attributes
        self.name = 'prototype'
        self.appearance = ''
        self.quest_item = 0
        #location
        self.location = ()
        self.level = None
        #icon
        self.icon = None
        self.weapon_data = None
        self.__effects_collection = effects_collection
        self.weight = None
        self.rarity = None
        self.cost = None
        self.tags = {}
        self.__update_listeners = []

    def __str__(self):
        return self.name

    @logged
    def get_name(self, character, decorate = False):
        """
        Get name of the item
        Name can be appearance or given name

        :param character: character handling the item
        :type character: Character
        :param decorate: should name be decorated with status info, default False
        :type decorate: Boolean
        """
        assert character != None

        if self.appearance != '':
            if self.name in character.item_memory.keys():
                name = character.item_memory[self.name]
            else:
                name = self.appearance
        else:
            name = self.name

        if decorate == True:
            if character.inventory.weapon == self:
                name = name + ' (weapon in hand)'

        return name

    def add_effect_handle(self, handle):
        """
        Adds an effect handle to an item

        :param handle: effect handle to add
        :type handle: EffectHandle

        .. versionadded:: 0.4
        """
        self.__effects_collection.add_effect_handle(handle)

    @logged
    def get_effect_handles(self, trigger = None):
        """
        Retrieves effects handles the item has

        :param trigger: type of effects retrieved. Default None
        :type trigger: string

        :returns: effect handles
        :rtype: [EffectHandle]

        .. versionadded:: 0.4
        """
        return self.__effects_collection.get_effect_handles(trigger)

    def __get_charges_left(self):
        """
        Amount of charges left in collection

        :returns: amount of charges
        :rtype: [integer]
        """
        return self.__effects_collection.get_charges_left()

    def __get_maximum_charges_left(self):
        """
        Return highest amount of charges left in collection

        :returns: highest charge
        :rtype: integer
        """
        return self.__effects_collection.get_maximum_charges_left()

    def __get_minimum_charges_left(self):
        """
        Return smallest amount of charges left in item

        :returns: smallest charge in collection
        :rtype: integer
        """
        return self.__effects_collection.get_minimum_charges_left()

    charges_left = property(__get_charges_left)
    maximum_charges_left = property(__get_maximum_charges_left)
    minimum_charges_left = property(__get_minimum_charges_left)

    @logged
    def get_main_type(self):
        """
        Return main type of the item

        :returns: main type
        :rtype: string
        """
        main_type = 'undefined'

        if 'weapon' in self.tags:
            main_type = 'weapon'
        elif 'potion' in self.tags:
            main_type = 'potion'
        elif 'food' in self.tags:
            main_type = 'food'

        return main_type

    @logged
    def get_tags(self):
        """
        Return tags
        """
        return self.tags

    @logged
    def register_for_updates(self, listener):
        """
        Register listener to receive updates for this entity

        :param listener: listener to add
        :type listener: Listener

        .. versionadded:: 0.5
        """
        self.__update_listeners.append(listener)

    @logged
    def remove_from_updates(self, listener):
        """
        Remove listener

        :param listener: listener to remove
        :type listener: Listener

        .. versionadded:: 0.5
        """
        self.__update_listeners.remove(listener)

    @logged
    def notify_update_listeners(self, event):
        """
        Notify all listeners registered for update of this entity

        :param event: event to relay to update listeners
        :type event: Event

        .. versionadded:: 0.5
        """
        for listener in self.__update_listeners:
            listener.receive_update(event)

class WeaponData(object):
    """
    Class representing weapon data of items
    """
    def __init__(self, damage = None, damage_type = None, critical_range = None,
                 critical_damage = None, weapon_type = None):
        """
        Default constructor

        :param damage: amount of damage
        :type damage: integer
        :param damage_type: type of damage
        :type damage_type: string
        :param critical_range: range where critical might occur
        :type critical_range: integer
        :param critical_damage: multiplier for critical damage
        :type critical_damage: integer
        :param weapon_type: type of weapon
        :type weapon_type: string
        """

        self.damage = damage
        self.damage_type = damage_type
        self.critical_range = critical_range
        self.critical_damage = critical_damage
        self.weapon_type = weapon_type

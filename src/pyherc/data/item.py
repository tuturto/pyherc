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
Module for item related classes

Classes:
    Item
    WeaponData
"""
from pyherc.aspects import log_debug


class Item():
    """
    Represents item
    """
    @log_debug
    def __init__(self, effects_collection):
        """
        Default constructor

        :param effects_collection: collection for effects
        :type effects_collection: EffectsCollection
        """
        super().__init__()
        #attributes
        self.name = 'prototype'
        self.description = 'prototype'
        self.appearance = ''
        self.quest_item = 0
        #location
        self.location = ()
        self.level = None
        #icon
        self.icon = None
        self.weapon_data = None
        self.armour_data = None
        self.ammunition_data = None
        self.__effects_collection = effects_collection
        self.weight = None
        self.rarity = None
        self.cost = None
        self.tags = {}
        self.__update_listeners = []

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        else:
            return 'uninitialized item'

    def __repr__(self):
        return str(self)

    @log_debug
    def get_name(self, character, decorate=False):
        """
        Get name of the item
        Name can be appearance or given name

        :param character: character handling the item
        :type character: Character
        :param decorate: should name be decorated with status info
        :type decorate: Boolean
        """
        assert character is not None

        if self.appearance != '':
            if self.name in character.item_memory:
                name = character.item_memory[self.name]
            else:
                name = self.appearance
        else:
            name = self.name

        if decorate:
            if self.ammunition_data is not None:
                name = name + ' ({0})'.format(self.ammunition_data.count)
            if character.inventory.weapon == self:
                name = name + ' (weapon in hand)'
            elif character.inventory.armour == self:
                name = name + ' (armour in use)'
            elif character.inventory.projectiles == self:
                name = name + ' (quivered)'

        return name

    @log_debug
    def add_effect_handle(self, handle):
        """
        Adds an effect handle to an item

        :param handle: effect handle to add
        :type handle: EffectHandle

        .. versionadded:: 0.4
        """
        self.__effects_collection.add_effect_handle(handle)

    @log_debug
    def get_effect_handles(self, trigger=None):
        """
        Retrieves effects handles the item has

        :param trigger: type of effects retrieved. Default None
        :type trigger: string

        :returns: effect handles
        :rtype: [EffectHandle]

        .. versionadded:: 0.4
        """
        return self.__effects_collection.get_effect_handles(trigger)

    @log_debug
    def __get_charges_left(self):
        """
        Amount of charges left in collection

        :returns: amount of charges
        :rtype: [integer]
        """
        return self.__effects_collection.get_charges_left()

    @log_debug
    def __get_maximum_charges_left(self):
        """
        Return highest amount of charges left in collection

        :returns: highest charge
        :rtype: integer
        """
        return self.__effects_collection.get_maximum_charges_left()

    @log_debug
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

    @log_debug
    def get_main_type(self):
        """
        Return main type of the item

        :returns: main type
        :rtype: string
        """
        main_type = 'undefined'

        if 'weapon' in self.tags:
            main_type = 'weapon'
        elif 'armour' in self.tags:
            main_type = 'armour'
        elif 'potion' in self.tags:
            main_type = 'potion'
        elif 'ammunition' in self.tags:
            main_type = 'ammunition'
        elif 'food' in self.tags:
            main_type = 'food'

        return main_type

    @log_debug
    def get_tags(self):
        """
        Return tags
        """
        return self.tags

    @log_debug
    def register_for_updates(self, listener):
        """
        Register listener to receive updates for this entity

        :param listener: listener to add
        :type listener: Listener

        .. versionadded:: 0.5
        """
        self.__update_listeners.append(listener)

    @log_debug
    def remove_from_updates(self, listener):
        """
        Remove listener

        :param listener: listener to remove
        :type listener: Listener

        .. versionadded:: 0.5
        """
        if listener in self.__update_listeners:
            self.__update_listeners.remove(listener)

    @log_debug
    def notify_update_listeners(self, event):
        """
        Notify all listeners registered for update of this entity

        :param event: event to relay to update listeners
        :type event: Event

        .. versionadded:: 0.5
        """
        for listener in self.__update_listeners:
            listener.receive_update(event)

    def _repr_pretty_(self, p, cycle):
        """
        Pretty print for IPython

        :param p: printer to write
        :param cycle: has pretty print detected a cycle?
        """
        if cycle:
            p.text('Item(...)')
        else:
            p.text('name: {0}'.format(self.name))
            p.breakable()
            p.text('location: {0}'.format(self.location))
            p.breakable()


class WeaponData():
    """
    Class representing weapon data of items
    """
    @log_debug
    def __init__(self, damage=None, critical_range=None,
                 critical_damage=None, weapon_type=None,
                 ammunition_type=None, speed=1.0):
        """
        Default constructor

        :param damage: array of amount and type of damage
        :type damage: [(integer, string), ...]
        :param critical_range: range where critical might occur
        :type critical_range: integer
        :param critical_damage: multiplier for critical damage
        :type critical_damage: integer
        :param weapon_type: type of weapon
        :type weapon_type: string
        :param speed: speed of the weapon
        :type speed: double
        """

        super().__init__()

        if damage is None:
            self.damage = []
        else:
            self.damage = damage

        self.critical_range = critical_range
        self.critical_damage = critical_damage
        self.weapon_type = weapon_type
        self.ammunition_type = ammunition_type
        self.speed = speed


class ArmourData():
    """
    Represents data of armours

    .. versionadded:: 0.8
    """
    @log_debug
    def __init__(self, damage_reduction=None, speed_modifier=None):
        """
        Default constructor

        :param damage_reduction: amount of damage reduced
        :type damage_reduction: int
        :param speed_modifier: modifier for speed of wearer
        :type speed_modifier: double
        """
        super().__init__()

        self.damage_reduction = damage_reduction
        self.speed_modifier = speed_modifier


class AmmunitionData():
    """
    Represents data of ammunition

    .. versionadded:: 0.8
    """
    @log_debug
    def __init__(self, damage=None, critical_range=None,
                 critical_damage=None, ammunition_type=None, count=1):
        """
        Default constructor
        """
        super().__init__()

        if damage is None:
            self.damage = []
        else:
            self.damage = damage

        self.critical_range = critical_range
        self.critical_damage = critical_damage
        self.ammunition_type = ammunition_type
        self.count = count

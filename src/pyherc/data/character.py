# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Module for Character related classes
"""
from pyherc.aspects import log_debug, log_info
from pyherc.rules import AttackParameters, DrinkParameters
from pyherc.rules import InventoryParameters, SpellCastingParameters
from pyherc.rules import GainDomainParameters
from pyherc.rules import WaitParameters
from pyherc.events import HitPointsChangedEvent, SpiritPointsChangedEvent
from pyherc.events import ErrorEvent
from pyherc.data.constants import NORMAL_ACTION
from decorator import decorator

@decorator
def guarded_action(wrapped_function, *args, **kwargs):
    """
    Decorator to guard against exceptions in action functions
    """
    try:
        return wrapped_function(*args, **kwargs)
    except Exception:
        self = args[0]
        self.tick = 10
        self.raise_event(ErrorEvent(self))

class Character():
    """
    Represents a character in playing world
    """
    @log_debug
    def __init__(self, model, effects_collection, inventory):
        """
        Default constructor

        :param model: model where character acts
        :type model: Model
        :param effects_collection: collection for effects
        :type effects_collection: EffectsCollection
        :param inventory: inventory for character
        :type inventory: Inventory
        """
        super(Character, self).__init__()
        # attributes
        self.model = model
        self.__body = None
        self.__finesse = None
        self.__mind = None
        self.name = 'prototype'
        self.race = None
        self.kit = None
        self.__hit_points = None
        self.__max_hp = None
        self.__spirit = 100
        self.max_spirit = 100
        self.speed = None
        self.inventory = inventory
        self.feats = []
        #location
        self.level = None
        self.location = ()
        #icon
        self.icon = None
        #internal
        self.tick = 0
        self.short_term_memory = []
        self.__event_listeners = []
        self.__update_listeners = []
        self.item_memory = {}
        self.size = 'medium'
        self.attack = None

        self.__active_effects = [] # active effects
        self.artificial_intelligence = None
        self.__effects_collection = effects_collection

    def __str__(self):
        return self.name

    @log_debug
    def receive_event(self, event):
        """
        Receives an event from world and enters it into short term memory

        :param event: event to receive
        :type event: Event
        """
        self.short_term_memory.append(event)

        for listener in self.__event_listeners:
            listener.receive_event(event)

    @log_debug
    def register_event_listener(self, listener):
        """
        Register event listener

        :param listener: listener to add
        :type listener: Listener

        .. versionadded:: 0.4
        """
        self.__event_listeners.append(listener)

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

    @guarded_action
    @log_info
    def act(self, model, action_factory, rng):
        """
        Triggers AI of this character

        :param model: model where character is located
        :type model: Model
        :param action_factory: factory for creating actions
        :type action_factory: ActionFactory
        :param rng: random number generator
        :type rng: Random
        """
        self.artificial_intelligence.act(model,
                                         action_factory,
                                         rng)

    def __get_hp(self):
        """
        Current hitpoints
        """
        return self.__hit_points

    def __set_hp(self, hit_points):
        """
        Current hitpoints
        """
        old_hit_points = self.__hit_points
        new_hit_points = hit_points

        self.__hit_points = hit_points

        self.raise_event(
            HitPointsChangedEvent(character = self,
                                  old_hit_points = old_hit_points,
                                  new_hit_points = new_hit_points))

    def __get_spirit(self):
        """
        Current spirit points
        """
        return self.__spirit

    def __set_spirit(self, spirit):
        old_spirit = self.__spirit
        new_spirit = spirit

        self.__spirit = spirit

        self.raise_event(
            SpiritPointsChangedEvent(character = self,
                                     old_spirit = old_spirit,
                                     new_spirit = new_spirit))

    def __get_body(self):
        """
        Current body attribute
        """
        return self.__body

    def __set_body(self, body):
        """
        Current body attribute
        """
        self.__body = body

    def __get_finesse(self):
        """
        Current finesse attribute
        """
        return self.__finesse

    def __set_finesse(self, finesse):
        """
        Current finesse attribute
        """
        self.__finesse = finesse

    def __get_mind(self):
        """
        Current mind attribute
        """
        return self.__mind

    def __set_mind(self, mind):
        """
        Current mind attribute
        """
        self.__mind = mind

    def get_attack(self):
        """
        Attack attribute of the character
        """
        return self.attack

    def set_attack(self, attack):
        """
        Attack attribute of the character
        """
        self.attack = attack

    def __get_max_hp(self):
        """
        Maximum HP this character can currently have
        """
        return self.__max_hp

    def __set_max_hp(self, max_hp):
        """
        Maximum HP this character can currently have
        """
        self.__max_hp = max_hp

    @log_debug
    def identify_item(self, item):
        """
        Identify item

        :param item: item to mark as identified
        :type item: Item
        """
        assert (item != None)
        self.item_memory[item.name] = item.name

    @log_debug
    def is_proficient(self, weapon):
        """
        Check if this character is proficient with a given weapon

        :param weapon: weapon which proficient requirements should be checked
        :type weapon: Item
        :returns: True if proficient, otherwise False
        :rtype: Boolean
        """
        assert weapon != None

        if weapon.weapon_data == None:
            return True

        if True in [(x.name == 'weapon proficiency'
                    and x.weapon_type == weapon.weapon_data.weapon_type)
                    and (x.weapon_name == None
                         or x.weapon_name == weapon.weapon_data.name)
                    for x in self.feats]:
            return True
        else:
            return False

    @log_debug
    def set_mimic_item(self, item):
        """
        Sets item this character can mimic or pretend to be

        :param item: item to mimic
        :type item: Item
        """
        self.mimic_item = item

    @log_debug
    def get_mimic_item(self):
        """
        Gets item this character can mimic

        :returns: item to mimic
        :rtype: Item
        """
        return self.mimic_item

    def get_location(self):
        """
        Returns location of this character

        :returns: location
        :rtype: (integer, integer)
        """
        return self.location

    def set_location(self, location):
        """
        Sets location of this character

        :param location: location to set
        :type location: (integer, integer)
        """
        self.location = location

    @guarded_action
    @log_info
    def execute_action(self, action_parameters, action_factory):
        """
        Execute action defined by action parameters

        :param action_parameters: parameters controlling creation of the action
        :type action_parameters: ActionParameters
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory
        """
        action = self.create_action(action_parameters,
                                    action_factory)
        action.execute()

    @log_debug
    def create_action(self, action_parameters, action_factory):
        """
        Create an action by defined by action parameters

        :param action_parameters: parameters controlling creation of the action
        :type action_parameters: ActionParameters
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory
        :returns: Action
        """
        action = action_factory.get_action(action_parameters)

        assert action != None

        return action

    @guarded_action
    @log_info
    def perform_attack(self, direction, action_factory, rng):
        """
        Attack to given direction

        :param direction: direction to attack
        :type direction: integer
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory
        :param rng: random number generator
        :type rng: Random
        """
        if self.inventory.weapon != None:
            weapon = self.inventory.weapon.weapon_data
            if self.inventory.projectiles != None:
                ammunition = self.inventory.projectiles.ammunition_data
            else:
                ammunition = None
        else:
            weapon = None

        if weapon == None:
            attack_type = 'unarmed'
        else:
            if (ammunition == None or
                    weapon.ammunition_type != ammunition.ammunition_type):
                attack_type = 'melee'
            else:
                target_loc = self.get_location_at_direction(direction)
                if self.level.get_creature_at(target_loc) == None:
                    if self.level.blocks_movement(target_loc[0], target_loc[1]):
                        attack_type = 'melee'
                    else:
                        attack_type = 'ranged'
                else:
                    attack_type = 'melee'

        action = action_factory.get_action(
                            AttackParameters(
                                attacker = self,
                                direction = direction,
                                attack_type = attack_type,
                                random_number_generator = rng))

        action.execute()

    @guarded_action
    @log_info
    def drink(self, potion, action_factory):
        """
        Drink potion

        :param potion: potion to drink
        :type potion: Item
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory
        """
        action = action_factory.get_action(
                                           DrinkParameters(
                                                           self,
                                                           potion))
        action.execute()

    @guarded_action
    @log_info
    def pick_up(self, item, action_factory):
        """
        Pick up item

        :param item: item to pick up
        :type item: Item
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory

        .. versionadded:: 0.4
        """
        action = action_factory.get_action(
                                    InventoryParameters(
                                                        self,
                                                        item,
                                                        'pick up'))
        action.execute()

    @guarded_action
    @log_info
    def drop_item(self, item, action_factory):
        """
        Drop item from inventory

        :param item: item to drop
        :type item: Item
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory

        .. versionadded:: 0.5
        """
        action = action_factory.get_action(
                                InventoryParameters(self,
                                                    item,
                                                    'drop'))
        action.execute()

    @guarded_action
    @log_info
    def equip(self, item, action_factory):
        """
        Wear item from inventory

        :param item: item to equip
        :type item: Item
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory

        .. versionadded:: 0.8
        """
        action = action_factory.get_action(
                                InventoryParameters(self,
                                                    item,
                                                    'equip'))
        action.execute()

    @guarded_action
    @log_info
    def unequip(self, item, action_factory):
        """
        Unequip item

        :param item: item to unequip
        :type item: Item
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory

        .. versionadded:: 0.8
        """
        action = action_factory.get_action(
                                InventoryParameters(self,
                                                    item,
                                                    'unequip'))
        action.execute()

    @guarded_action
    @log_info
    def cast(self, direction, spell_name, action_factory):
        """
        Cast a spell

        :param direction: direction to cast the spell
        :type direction: int
        :param spell: spell to cast
        :type spell: string
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory

        .. versionadded:: 0.9
        """
        action = action_factory.get_action(
                                SpellCastingParameters(self,
                                                       direction = direction,
                                                       spell_name = spell_name))
        if action.is_legal():
            action.execute()

    @guarded_action
    @log_info
    def wait(self, action_factory):
        """
        Wait for a bit

        :param action_factory: factory to create actions
        :type action_factory: ActionFactory

        .. versionadded:: 0.10
        """
        action = action_factory.get_action(
                                    WaitParameters(self,
                                                   NORMAL_ACTION))
        if action.is_legal():
            action.execute()

    @guarded_action
    @log_info
    def gain_domain(self, action_factory, domain, item):
        """
        Sacrifice an item to gain a domain

        :param action_factory: factory to create actions
        :type action_factory: ActionFactory
        :param domain: name of the domain to gain
        :type domain: String
        :param item: item to sacrifice
        :type item: Item

        .. versionadded:: 0.10
        """
        action = action_factory.get_action(
                            GainDomainParameters(character = self,
                                                 domain = domain,
                                                 item = item))

        if action.is_legal():
            action.execute()

    @log_debug
    def raise_event(self, event):
        """
        Raise event for other creatures to see

        :param event: event to raise
        :type event: Event
        """
        self.model.raise_event(event)
        self.notify_update_listeners(event)

    @log_debug
    def add_effect_handle(self, effect):
        """
        Adds an effect handle to an character

        :param effect: effect to add
        :type effect: EffectHandle

        .. versionadded:: 0.4
        """
        self.__effects_collection.add_effect_handle(effect)

    @log_debug
    def get_effect_handles(self, trigger = None):
        """
        Get effect handles

        :param trigger: optional trigger type
        :type trigger: string

        :returns: effect handles
        :rtype: [EffectHandle]

        .. versionadded:: 0.4
        """
        return self.__effects_collection.get_effect_handles(trigger)

    @log_debug
    def remove_effect_handle(self, handle):
        """
        Remove given handle

        :param handle: handle to remove
        :type handle: EffectHandle

        .. versionadded:: 0.4
        """
        self.__effects_collection.remove_effect_handle(handle)

    @log_debug
    def add_effect(self, effect):
        """
        Adds effect to this character

        :param effect: Effect to add
        :type effect: Effect

        .. note: Multiples of same type of effect are not added
        .. versionadded:: 0.4
        """
        if effect.multiple_allowed == False:
            if not self.__effects_collection.has_effect(effect):
                self.__effects_collection.add_effect(effect)
                self.raise_event(effect.get_add_event())
        else:
            self.__effects_collection.add_effect(effect)
            self.raise_event(effect.get_add_event())

    @log_debug
    def get_effects(self):
        """
        Get effects of the character

        :returns: effects
        :rtype: [Effect]

        .. versionadded:: 0.4
        """
        return self.__effects_collection.get_effects()

    @log_debug
    def remove_expired_effects(self):
        """
        Remove all effects that have expired

        .. versionadded:: 0.4
        """
        removed = self.__effects_collection.get_expired_effects()

        if len(removed) > 0:
            self.__effects_collection.remove_expired_effects()
            for effect in removed:
                self.raise_event(effect.get_removal_event())

    def add_to_tick(self, cost):
        """
        Add cost of action to characters tick,
        while taking characters speed into account

        :param cost: Cost of action in ticks
        :type cost: integer
        """
        self.tick = self.tick + (self.speed * cost)

    @log_debug
    def get_location_at_direction(self, direction):
        """
        Get location next to this character at given direction

        :param direction: direction to check
        :type direction: int
        :returns: coordinates of location
        :rtype: (int, int)

        .. note:: values 1 to 8 are supported for direction
        """
        assert direction <= 8
        assert direction >= 1

        offset = [(0, 0),
                  (0, -1), (1, -1), (1, 0), (1, 1),
                  (0, 1), (-1, 1), (-1, 0), (-1, -1)]

        return tuple(x for x in
                     map(sum, zip(self.location, offset[direction])))

    def _repr_pretty_(self, p, cycle):
        """
        Pretty print for IPython

        :param p: printer to write
        :param cycle: has pretty print detected a cycle?
        """
        if cycle:
            p.text('Character(...)')
        else:
            p.text('name: {0}'.format(self.name))
            p.breakable()
            p.text('hitpoints: {0}/{1}'.format(self.__hit_points,
                                                    self.__max_hp))
            p.breakable()
            p.text('body: {0}'.format(self.__body))
            p.breakable()
            p.text('finesse: {0}'.format(self.__finesse))
            p.breakable()
            p.text('mind: {0}'.format(self.__mind))
            p.breakable()
            p.text('location: {0}'.format(self.location))
            p.breakable()
            p.pretty(self.inventory)
            p.breakable()
            p.pretty(self.__effects_collection)
            p.breakable()

    hit_points = property(__get_hp, __set_hp)
    spirit = property(__get_spirit, __set_spirit)
    max_hp = property(__get_max_hp, __set_max_hp)
    body = property(__get_body, __set_body)
    finesse = property(__get_finesse, __set_finesse)
    mind = property(__get_mind, __set_mind)

class Feat():
    """
    Represents a feat that a character can have
    """
    @log_debug
    def __init__(self, name = None, target = None):
        self.name = name
        self.target = target

class WeaponProficiency(Feat):
    """
    Represents weapon proficiency feats (proficiency, focus, etc.)
    """
    @log_debug
    def __init__(self, weapon_type = 'simple', weapon_name = None):
        Feat.__init__(self, weapon_type, weapon_name)

        self.name = 'weapon proficiency'
        self.weapon_type = weapon_type
        self.weapon_name = weapon_name

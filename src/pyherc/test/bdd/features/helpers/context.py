# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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
Module for general context helpers
"""
from pyherc.data import Model
from pyherc.ports import ActionsPort
from pyherc.test.builders import ActionFactoryBuilder
from pyherc.test.cutesy import (Arrows, Bow, Club, Dagger, LeatherArmour,
                                PlateMail, Rune, ScaleMail, Sword, Warhammer)


def default_context(fn):
    """
    Decorator to set up context

    .. versionadded:: 0.8
    """
    def context_setup(*args, **kwargs):
        """
        Set up context
        """
        context = args[0]

        if not hasattr(context, 'model'):
            context.model = Model()

        if not hasattr(context, 'items'):
            context.items = []

        if not hasattr(context, 'characters'):
            context.characters = []

        if not hasattr(context, 'places'):
            context.places = []

        return fn(*args, **kwargs)

    return context_setup


def with_action_factory(fn):
    """
    Decorator to inject action factory

    .. versionadded:: 0.8
    """
    def action_factorize(*args, **kwargs):
        """
        Inject action factory
        """
        context = args[0]

        if not hasattr(context, 'action_factory'):
            context.action_factory = (ActionFactoryBuilder()
                                      .with_move_factory()
                                      .with_attack_factory()
                                      .with_drink_factory()
                                      .with_inventory_factory()
                                      .with_dying_rules()
                                      .build())

        if not hasattr(context, 'actions_port'):
            context.actions_port = ActionsPort(context.action_factory)

        return fn(*args, **kwargs)

    return action_factorize


def armour_list(fn):
    """
    Decorator to set up armour list

    .. versionadded:: 0.8
    """
    def armour_setup(*args, **kwargs):
        """
        Set up armour list
        """
        context = args[0]

        if not hasattr(context, 'armour_list'):
            context.armour_list = {}
            context.armour_list['leather armour'] = LeatherArmour
            context.armour_list['scale mail'] = ScaleMail
            context.armour_list['plate mail'] = PlateMail

        return fn(*args, **kwargs)

    return armour_setup


def weapon_list(fn):
    """
    Decorator to set up weapon list

    .. versionadded:: 0.8
    """
    def weapon_setup(*args, **kwargs):
        """
        Setup weapon list
        """
        context = args[0]

        if not hasattr(context, 'weapon_list'):
            context.weapon_list = {}
            context.weapon_list['warhammer'] = Warhammer
            context.weapon_list['sword'] = Sword
            context.weapon_list['dagger'] = Dagger
            context.weapon_list['club'] = Club
            context.weapon_list['bow'] = Bow
            context.weapon_list['arrows'] = Arrows

        return fn(*args, **kwargs)

    return weapon_setup


def misc_item_list(fn):
    """
    Decorator to set up misc items list

    .. versionadded:: 0.10
    """
    def misc_item_setup(*args, **kwargs):
        """
        Setup misc items list
        """
        context = args[0]

        if not hasattr(context, 'misc_item_list'):
            context.misc_item_list = {}
            context.misc_item_list['rune'] = Rune

        return fn(*args, **kwargs)

    return misc_item_setup


def get_character(context, character_name):
    """
    Get character from context

    :param context: context
    :param character_name: name of character
    :type character_name: string

    .. versionadded:: 0.8
    """
    characters = [x for x in context.characters
                  if x.name == character_name]
    return characters[0]


def get_location(context, location_name):
    """
    Get location from context

    :param context: context
    :param location_name: name of location
    :type location_name: string

    .. versionadded:: 0.8
    """
    locations = [x for x in context.places
                 if ((hasattr(x, 'name') and x.name == location_name)
                     or (hasattr(x, 'keys') and x['name'] == location_name))]
    return locations[0]


def get_item(context, item_name):
    """
    Get item from context

    :param context: context
    :param item_name: name of item
    :type item_name: string

    .. versionadded:: 0.8
    """
    items = [x for x in context.items
             if x.name == item_name]
    return items[0]


def get_entity(context, entity_name):
    """
    Get entity from context

    :param context: context
    :param entity_name: name of entity
    :type entity_name: string

    .. versionadded:: 0.8
    """
    entities = []
    entities.extend(context.characters)
    entities.extend(context.items)

    entity = [x for x in entities
              if x.name == entity_name]

    if entity:
        return entity[0]
    else:
        return get_location(context, entity_name)

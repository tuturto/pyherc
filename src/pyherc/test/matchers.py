#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
Module for customer matchers used in testing
"""

from hamcrest import * #pylint: disable=W0401
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

class MapConnectivity():
    """
    Helper class used to verify if generated level is fully connected
    """
    def __init__(self, open_tile):
        """
        Initialise this matcher
        """
        self.open_tile = open_tile

    def _matches(self, item):
        all_points = self.get_all_points(item, self.open_tile)

        if len(all_points) > 0:
            connected_points = self.get_connected_points(item,
                                                         all_points[0],
                                                         self.open_tile,
                                                         [])
            connected = True
            for point in all_points:
                if not point in connected_points:
                    connected = False
        else:
            connected = False

        return connected

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append(
                'Level')

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Unconnected level')

    def get_all_points(self, level, open_tile):
        """
        Get all open points in level

        Args:
            open: ID of tile considered open

        Returns:
            List of all open points in level
        """
        points = []

        for loc_y in range(len(level.walls[0])):
            for loc_x in range(len(level.walls)):
                if level.walls[loc_x][loc_y] == open_tile:
                    points.append((loc_x, loc_y))

        return points

    def get_connected_points(self, level, start, open_tile, connected_points):
        """
        Get all points that are connected to a given point

        Args:
            level: level to check
            start: start location
            open: ID of tile considered open

        Returns:
            list of connected points
        """
        x_loc = start[0]
        y_loc = start[1]

        if start in connected_points:
            return None

        if x_loc < 0 or x_loc > len(level.walls) - 1:
            return None

        if y_loc < 0 or y_loc > len(level.walls[0]) - 1:
            return None

        if level.get_wall_tile(x_loc, y_loc) == open_tile:
            connected_points.append(start)
            self.get_connected_points(level, (x_loc, y_loc - 1), open_tile, connected_points)
            self.get_connected_points(level, (x_loc, y_loc + 1), open_tile, connected_points)
            self.get_connected_points(level, (x_loc - 1, y_loc), open_tile, connected_points)
            self.get_connected_points(level, (x_loc + 1, y_loc), open_tile, connected_points)

        return connected_points

def is_fully_accessible_via(open_tile):
    return MapConnectivity(open_tile)

def located_in_room(entity):
    """
    Check if given entity is located in room

    Args:
        entity: entity to check

    Returns:
        True if located in room, False otherwise

    Note:
        entity should have properties level and location for this to work
    """
    level = entity.level

    if level.get_location_type(entity.location) == 'room':
        return True
    else:
        return False

class ContainsCreature(BaseMatcher):
    """
    Class to check if given level has creatures
    """
    def __init__(self, creature, amount):
        """
        Default constructor
        """
        self.creature = creature
        self.amount = amount

    def _matches(self, item):
        """
        Check for match
        """
        count = 0

        for creature in item.creatures:
            if creature.name == self.creature:
                count = count + 1

        return self.amount.matches(count)

    def describe_to(self, description):
        """
        Describe this matcher
        """
        if self.amount == None:
            description.append(
                    'Level with creature named {0}'
                    .format(self.creature))
        else:
            description.append(
                    'Level with {0} creatures named {1}'
                    .format(self.amount, self.creature))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        names = [x.name for x in item.creatures]

        mismatch_description.append('Was level with creatures {0}'
                                    .format(names))

class ActiveEffects(BaseMatcher):
    """
    Class to check amount of active effects
    """
    def __init__(self, amount_of_effects):
        """
        Default constructor
        """
        self.amount_of_effects = amount_of_effects

    def _matches(self, item):
        return self.amount_of_effects.matches(len(item.active_effects))

    def describe_to(self, description):
        description.append(
                    'Object with {0} active effects'
                    .format(self.amount_of_effects))

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append('Was object with {0} active effects'
                                    .format(len(item.active_effects)))

class ActiveEffectInstance(BaseMatcher):
    """
    Class to check amount of active effects
    """
    def __init__(self, effect):
        """
        Default constructor
        """
        self.effect = effect

    def _matches(self, item):
        for effect in item.active_effects:
            if effect == self.effect:
                return True
        return False

    def describe_to(self, description):
        description.append(
                    'Object with active effects containing {0}'
                    .format(self.effect))

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append('Was object with active effects {0}'
                                    .format(item.active_effects))

def has_active_effects(amount_of_effects):
    return ActiveEffects(wrap_matcher(amount_of_effects))

def has_no_active_effects():
    return ActiveEffects(wrap_matcher(0))

def has_active_effect(effect):
    return ActiveEffectInstance(effect)

def has_creature(creature, amount):
    """
    Check if level has given creature

    Args:
        creature: Name of the creature to check
        amount: Amount of creatures to expect
    """
    return ContainsCreature(creature, wrap_matcher(amount))

class ContainsItem(BaseMatcher):
    """
    Class to check if given level has Items
    """
    def __init__(self, item, amount):
        """
        Default constructor
        """
        self.item = item
        self.amount = amount

    def _matches(self, item):
        """
        Check for match
        """
        count = 0

        for item in item.items:
            if item.name == self.item:
                count = count + 1

        return self.amount.matches(count)

    def describe_to(self, description):
        """
        Describe this matcher
        """
        if self.amount == None:
            description.append(
                    'Level with item named {0}'
                    .format(self.item))
        else:
            description.append(
                    'Level with {0} items named {1}'
                    .format(self.amount, self.item))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        names = [x.name for x in item.items]

        mismatch_description.append('Was level with items {0}'
                                    .format(names))

def does_have_item(item, amount):
    """
    Check if level has given item

    Args:
        item: Name of the item to check
        amount: Amount of items to expect
    """
    return ContainsItem(item, wrap_matcher(amount))

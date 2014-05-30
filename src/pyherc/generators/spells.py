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
Module for spell factory
"""
from functools import partial

from pyherc.aspects import log_debug, log_info
from pyherc.data.effects import EffectHandle
from pyherc.data.geometry import get_target_in_direction, TargetData
from pyherc.data import blocks_los, get_character
from pyherc.data.magic import Spell
from pyherc.rules.los import get_fov_matrix


class SpellGenerator():
    """
    Factory for creating spells

    .. versionadded:: 0.9
    """
    @log_debug
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.spell_list = {}

        self.__init_spells()

    @log_debug
    def __init_spells(self):
        """
        Temporary implementation for spell loading
        """

        healing_spell = SpellSpecification([
            EffectHandle(trigger='on spell hit',
                         effect='heal medium wounds',
                         parameters=None,
                         charges=1)],
            targeting_caster,
            spirit=5)

        magic_missile = SpellSpecification([
            EffectHandle(trigger='on spell hit',
                         effect='cause wound',
                         parameters=None,
                         charges=1)],
            targeting_single_target,
            spirit=7)

        fireball = SpellSpecification([
            EffectHandle(trigger='on spell hit',
                         effect='fire',
                         parameters=None,
                         charges=1),
            EffectHandle(trigger='on spell hit',
                         effect='cause wound',
                         parameters=None,
                         charges=1)],
            partial(targeting_spherical_area, radius=3),
            spirit=10)

        self.spell_list['healing wind'] = healing_spell
        self.spell_list['magic missile'] = magic_missile
        self.spell_list['fireball'] = fireball

    @log_info
    def create_spell(self, spell_name, targets):
        """
        Create a spell

        :param spell_name: name of the spell
        :type spell_name: string
        :param target: target of the spell
        :type target: Character
        :returns: ready to use spell
        :rtype: Spell
        """
        new_spell = Spell()
        new_spell.targets.extend(targets)

        spec = self.spell_list[spell_name]
        new_spell.spirit = spec.spirit
        handles = spec.effect_handles

        for effect_handle in handles:
            new_spell.add_effect_handle(effect_handle)

        return new_spell


class SpellSpecification():
    """
    Class to specify spell configuration

    .. versionadded:: 0.9
    """

    @log_debug
    def __init__(self, effect_handles, targeter, spirit):
        super().__init__()
        self.effect_handles = effect_handles
        self.targeter = targeter
        self.spirit = spirit


def targeting_caster(parameters):
    """
    Function to target the caster

    .. versionadded:: 0.9
    """
    return [TargetData('character',
                       parameters.caster.location,
                       parameters.caster,
                       None)]


@log_info
def targeting_single_target(parameters):
    """
    Function to target a single character in direction

    .. versionadded:: 0.9
    """
    target = get_target_in_direction(level=parameters.caster.level,
                                     location=parameters.caster.location,
                                     direction=parameters.direction)
    if target:
        return [target]
    else:
        return []


@log_info
def targeting_spherical_area(parameters, radius):
    """
    Function to target a spherical area

    .. versionadded:: 0.10
    """
    targets = []
    initial = get_target_in_direction(level=parameters.caster.level,
                                      location=parameters.caster.location,
                                      direction=parameters.direction)

    if initial and initial.previous_target:
        splash_center = initial.previous_target.location
        level = parameters.caster.level

        matrix = get_fov_matrix(splash_center,
                                level,
                                radius)

        x_range = range(splash_center[0] - radius,
                        splash_center[0] + radius + 1)

        y_range = range(splash_center[1] - radius,
                        splash_center[1] + radius + 1)

        for location, is_visible in matrix.items():
            if is_visible:
                creature = get_character(level, location)
                if creature:
                    targets.append(TargetData('character',
                                              location,
                                              creature,
                                              None))
                elif blocks_los(level, location):
                    targets.append(TargetData('wall',
                                              location,
                                              None,
                                              None))
                else:
                    targets.append(TargetData('void',
                                              location,
                                              None,
                                              None))

    return targets

#!/usr/bin/env python3
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
Module for spell factory
"""
from pyherc.aspects import logged

from pyherc.data.magic import Spell
from pyherc.data.effects import EffectHandle
from pyherc.data.geometry import get_target_in_direction

class SpellGenerator():
    """
    Factory for creating spells
    
    .. versionadded:: 0.9
    """
    @logged
    def __init__(self):
        """
        Default constructor
        """
        self.spell_list = {}

        self.__init_spells()

    @logged
    def __init_spells(self):
        """
        Temporary implementation for spell loading
        """

        healing_spell = SpellSpecification([
                              EffectHandle(trigger = 'on spell hit',
                                           effect = 'heal medium wounds',
                                           parameters = None,
                                           charges = 1)],
                              targeting_caster)

        magic_missile = SpellSpecification([
                            EffectHandle(trigger = 'on spell hit',
                                         effect = 'cause wound',
                                         parameters = None,
                                         charges = 1)],
                            targeting_single_target)

        fireball = SpellSpecification([
                            EffectHandle(trigger = 'on spell hit',
                                         effect = 'fire',
                                         parameters = None,
                                         charges = 1)],
                            targeting_spherical_area)

        self.spell_list['healing wind'] = healing_spell
        self.spell_list['magic missile'] = magic_missile
        self.spell_list['fireball'] = fireball
    
    @logged
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
        handles = spec.effect_handles
        
        for effect_handle in handles:
            new_spell.add_effect_handle(effect_handle)

        return new_spell

class SpellSpecification():
    """
    Class to specify spell configuration

    .. versionadded:: 0.9
    """
    def __init__(self, effect_handles, targeter):
        self.effect_handles = effect_handles
        self.targeter = targeter
    
def targeting_caster(parameters):
    """
    Function to target the caster

    .. versionadded:: 0.9
    """
    return [parameters.caster]

def targeting_single_target(parameters):
    """
    Function to target a single character in direction

    .. versionadded:: 0.9
    """
    target = get_target_in_direction(level = parameters.caster.level,
                                     location = parameters.caster.location,
                                     direction = parameters.direction)
    return [target]

def targeting_spherical_area(parameters):
    """
    Function to target a spherical area

    .. versionadded:: 0.10
    """
    return []

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
Module for SpellFactoryBuilder
"""
from pyherc.generators import SpellGenerator
from pyherc.data.magic import Spell
from pyherc.data.geometry import TargetData

class SpellGeneratorBuilder():
    """
    Builder for SpellFactory
    
    .. versionadded:: 0.9
    """
    def __init__(self):
        """
        Default constructor
        """
        pass
    
    def build(self):
        """
        Builds the factory
        """
        return SpellGenerator()

class SpellBuilder():
    """
    Builder for single spells

    .. versionadded:: 0.9
    """
    def __init__(self):
        """
        Default constructor
        """
        self.spirit = 5
        self.handles = []
        self.targets = []

    def with_effect_handle(self, handle):
        """
        Configure spell to use an effect handle

        :param handle: effect handle to add
        :type handle: EffectHandle

        .. note:: Can be called multiple times
        """
        self.handles.append(handle)
        return self

    def with_target(self, target):
        """
        Configure target of the spell

        :param target: target of the spell
        :type target: Character

        .. note:: Can be called multiple times
        """
        self.targets.append(target)
        return self

    def with_spirit(self, spirit):
        """
        Configure amount of spirit this spell takes

        :param spirit: amount of spirit the spell requires
        :type spirit: int

        .. versionadded:: 0.10
        """
        self.spirit = spirit
        return self

    def build(self):
        """
        Builds a spell

        :returns: a spell
        :rtype: Spell
        """
        spell = Spell()
        spell.spirit = self.spirit

        for handle in self.handles:
            spell.add_effect_handle(handle)

        for target in self.targets:
            spell.targets.append(TargetData('character',
                                            target.location,
                                            target,
                                            None))

        return spell

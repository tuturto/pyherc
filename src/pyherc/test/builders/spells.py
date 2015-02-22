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
Module for SpellFactoryBuilder
"""
from pyherc.data.geometry import TargetData
from pyherc.data.magic import Spell, SpellEntry
from pyherc.generators import SpellGenerator


class SpellGeneratorBuilder():
    """
    Builder for SpellFactory

    .. versionadded:: 0.9
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

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
        super().__init__()
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


class SpellEntryBuilder():
    """
    Builder for making spell entries for spell book

    .. versionadded:: 0.10
    """

    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.spell_name = 'prototype'
        self.level = 1
        self.domain = 'prototype'

    def with_name(self, name):
        """
        Configure name of the spell

        :param name: name of the spell
        :type name: String
        """
        self.spell_name = name
        return self

    def with_domain(self, domain, level):
        """
        Configure domain of the spell

        :param domain: name of the domain
        :type domain: String
        :param level: required level
        :type level: int
        """
        self.level = level
        self.domain = domain
        return self

    def build(self):
        """
        Build this spell entry

        :returns: fully configured spell entry
        :rtype: SpellEntry
        """
        new_entry = SpellEntry()
        new_entry.spell_name = self.spell_name
        new_entry.domain = self.domain
        new_entry.level = self.level

        return new_entry

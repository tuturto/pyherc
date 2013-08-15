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
Module defining spell casting actions
"""
from pyherc.aspects import log_debug, log_info

class SpellCastingAction():
    """
    Action for casting a spell

    .. versionadded:: 0.9
    """
    @log_debug
    def __init__(self, caster, spell, effects_factory, dying_rules):
        """
        Default constructor

        :param caster: character casting the spell
        :type caster: Character
        :param spell: spell being cast
        :type spell: Spell
        :param effects_factory: factory for creating effects
        :type effects_factory: EffectsFactory
        :param dying_rules: rules for dying
        :type dying_rules: DyingRules
        """
        self.caster = caster
        self.spell = spell
        self.effects_factory = effects_factory
        self.dying_rules = dying_rules

    @log_info
    def execute(self):
        """
        Executes this action
        """
        self.spell.cast(effects_factory = self.effects_factory,
                        dying_rules = self.dying_rules)

    @log_debug
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if casting spell is possible, false otherwise
        :rtype: Boolean
        """
        return True

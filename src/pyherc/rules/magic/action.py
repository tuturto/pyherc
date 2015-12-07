# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
        super().__init__()
        self.caster = caster
        self.spell = spell
        self.effects_factory = effects_factory
        self.dying_rules = dying_rules

    @log_info
    def execute(self):
        """
        Executes this action
        """
        self.caster.spirit = self.caster.spirit - self.spell.spirit

        self.spell.cast(effects_factory=self.effects_factory,
                        dying_rules=self.dying_rules)

    @log_debug
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if casting spell is possible, false otherwise
        :rtype: Boolean
        """
        return self.caster.spirit - self.spell.spirit >= 0


class GainDomainAction():
    """
    Action for gaining a domain

    .. versionadded:: 0.10
    """
    @log_debug
    def __init__(self, character, item, domain):
        """
        Default constructor

        :param character: character gaining a domain
        :type character: Character
        :param item: item to sacrifice
        :type item: Item
        :param domain: domain to gain
        :type domain: string
        """
        super().__init__()
        self.character = character
        self.item = item
        self.domain = domain

    @log_info
    def execute(self):
        """
        Executes this action
        """
        self.character.add_domain_level(domain=self.domain)

    @log_debug
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if gaining a domain is possible
        :rtype: Boolean
        """
        return True

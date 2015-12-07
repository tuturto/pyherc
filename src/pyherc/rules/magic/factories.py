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
Spell casting related factories
"""
from pyherc.aspects import log_debug, log_info
from pyherc.rules.factory import SubActionFactory
from pyherc.rules.magic.action import GainDomainAction, SpellCastingAction


class SpellCastingFactory(SubActionFactory):
    """
    Factory for creating spell casting actions

    .. versionadded:: 0.9
    """
    @log_debug
    def __init__(self, spell_factory, effects_factory, dying_rules):
        """
        Constructor for this factory
        """
        super().__init__()
        self.spell_factory = spell_factory
        self.effects_factory = effects_factory
        self.dying_rules = dying_rules
        self.action_type = 'spell casting'

    @log_info
    def get_action(self, parameters):
        """
        Create a spell casting action

        :param parameters: parameters used to control creation
        :type parameters: SpellCastingParameters
        """
        spell = self.spell_factory.create_spell(
            spell_name=parameters.spell_name,
            targets=self._get_spell_targets(parameters))

        return SpellCastingAction(caster=parameters.caster,
                                  spell=spell,
                                  effects_factory=self.effects_factory,
                                  dying_rules=self.dying_rules)

    @log_debug
    def _get_spell_targets(self, parameters):
        """
        Get targets for spell

        :returns: targets of a spell
        :rtype: [Character]
        """
        spec = self.spell_factory.spell_list[parameters.spell_name]
        return spec.targeter(parameters)


class GainDomainFactory(SubActionFactory):
    """
    Factory for creating gain domain actions

    .. versionadded:: 0.10
    """
    @log_debug
    def __init__(self):
        """
        Constructor for this factory
        """
        super().__init__()
        self.action_type = 'gain domain'

    @log_info
    def get_action(self, parameters):
        """
        Create a gain domain action

        :param parameters: parameters used to control creation
        :type parameters: GainDomainParameters
        """
        return GainDomainAction(character=parameters.character,
                                item=parameters.item,
                                domain=parameters.domain)

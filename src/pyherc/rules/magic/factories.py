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

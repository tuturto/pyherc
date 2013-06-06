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
Spell casting related factories
"""
from pyherc.rules.factory import SubActionFactory
from pyherc.rules.magic.action import SpellCastingAction
from pyherc.aspects import logged

class SpellCastingFactory(SubActionFactory):
    """
    Factory for creating spell casting actions

    .. versionadded:: 0.9
    """
    @logged
    def __init__(self, spell_factory):
        """
        Constructor for this factory
        """
        self.spell_factory = spell_factory
        self.action_type = 'spell casting'

    @logged
    def get_action(self, parameters):
        """
        Create a spell casting action

        :param parameters: parameters used to control creation
        :type parameters: SpellCastingParameters
        """
        spell = self.spell_factory.create_spell(spell_name = parameters.spell_name,
                                                target = parameters.caster)
        
        return SpellCastingAction(caster = parameters.caster,
                                  spell = spell)

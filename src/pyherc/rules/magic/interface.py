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
Public interface for magic rules package
"""

from pyherc.aspects import log_debug, log_info
from pyherc.rules.public import ActionParameters


@log_info
def cast(character, direction, spell_name, action_factory):
    """
    Cast a spell

    :param character: character casting the spell
    :type character: Character
    :param direction: direction to cast the spell
    :type direction: int
    :param spell: spell to cast
    :type spell: string
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory

    .. versionadded:: 0.9
    """
    action = action_factory.get_action(
        SpellCastingParameters(caster=character,
                               direction=direction,
                               spell_name=spell_name))

    if action.is_legal():
        action.execute()


@log_info
def gain_domain(character, action_factory, domain, item):
    """
    Sacrifice an item to gain a domain

    :param action_factory: factory to create actions
    :type action_factory: ActionFactory
    :param domain: name of the domain to gain
    :type domain: String
    :param item: item to sacrifice
    :type item: Item

    .. versionadded:: 0.10
    """
    action = action_factory.get_action(GainDomainParameters(character,
                                                            domain,
                                                            item))

    if action.is_legal():
        action.execute()


class SpellCastingParameters(ActionParameters):
    """
    Class for controlling spell casting

    .. versionadded:: 0.9
    """

    @log_debug
    def __init__(self, caster, direction, spell_name):
        """
        Construct spell casting parameters

        :param caster: character casting the spell
        :type caster: Character
        :param direction: direction to which the spell is cast
        :type direction: int
        :param spell_name: name of the spell
        :type spell_name: string
        """
        super().__init__()

        self.action_type = 'spell casting'
        self.caster = caster
        self.direction = direction
        self.spell_name = spell_name


class GainDomainParameters(ActionParameters):
    """
    Class for controlling gaining a domain

    .. versionadded:: 0.10
    """
    @log_debug
    def __init__(self, character, item, domain):
        """
        Construct gain domain parameter

        :param character: character to gain a domain
        :type character: Character
        :param item: item to sacrifice
        :type item: Item
        :param domain: domain to gain
        :type domain: String
        """
        super().__init__()

        self.action_type = 'gain domain'
        self.character = character
        self.item = item
        self.domain = domain

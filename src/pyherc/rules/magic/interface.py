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

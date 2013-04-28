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
from pyherc.aspects import logged

class SpellCastingAction():
    """
    Action for casting a spell

    .. versionadded:: 0.9
    """
    @logged
    def __init__(self, caster, direction, spell):
        """
        Default constructor

        :param caster: character casting the spell
        :type caster: Character
        :param direction: direction of the spell
        :type direction: int
        :param spell: spell to cast
        :type spell_name: Spell
        """
        self.caster = caster
        self.direction = direction
        self.spell = spell

    @logged
    def execute(self):
        """
        Executes this action
        """
        pass

    @logged
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if casting spell is possible, false otherwise
        :rtype: Boolean
        """
        return False

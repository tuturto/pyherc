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
Module for spell book related classes
"""

from pyherc.aspects import log_debug, log_info

class SpellBook():
    """
    List of known spells

    .. versionadded:: 0.10
    """

    @log_info
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.domains = {}

    @log_debug
    def add_spell_level(self, domain, level=None):
        """
        Add level to a spell domain

        :param domain: name of domain to learn
        :type domain: string
        :param level: new level of domain
        :type level: int

        .. note:: if level is None, current level is incremented by one
        """
        if not level:
            level = 1

        if domain in self.domains:
            self.domains[domain] = self.domains[domain] + level
        else:
            self.domains[domain] = level

    @log_debug
    def get_spell_level(self, domain):
        """
        Get current spell level of a given domain

        :param domain: name of the domain
        :type domain: String
        :returns: current level, 0 if domain is unknown
        :rtype: int

        .. versionadded:: 0.10
        """
        if domain in self.domains:
            return self.domains[domain]
        else:
            return 0

class SpellEntry():
    """
    Entry in a spell book

    .. versionadded:: 0.10
    """
    def __init__():
        """
        Default constructor
        """
        super().__init__()


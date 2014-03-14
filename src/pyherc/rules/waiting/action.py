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
Module defining wait related actions
"""
from pyherc.aspects import log_debug, log_info


class WaitAction():
    """
    Action for waiting

    .. versionadded:: 0.10
    """
    @log_debug
    def __init__(self, character, time_to_wait):
        """
        Default constructor

        :param character: character waiting
        :type character: Character
        :param time_to_wait: amount of ticks to wait
        :type time_to_wait: int
        """
        super().__init__()
        self.character = character
        self.time_to_wait = time_to_wait

    @log_info
    def execute(self):
        """
        Executes this action
        """
        self.character.tick = self.character.tick + self.time_to_wait

    @log_debug
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if waiting is possible, false otherwise
        :rtype: Boolean
        """
        return True

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
Public interface for wait actions
"""

from pyherc.aspects import log_debug, log_info
from pyherc.data import Duration
from pyherc.rules.public import ActionParameters


@log_info
def wait(character, action_factory):
    """
    Wait for a bit

    :param character: character doing waiting
    :type character: Character
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory

    .. versionadded:: 0.10
    """
    action = action_factory.get_action(WaitParameters(character,
                                                      Duration.normal))
    if action.is_legal():
        action.execute()


class WaitParameters(ActionParameters):
    """
    Class for controlling waiting

    .. versionadded:: 0.10
    """
    @log_debug
    def __init__(self, character, time_to_wait):
        """
        Construct wait parameters

        :param character: character to wait
        :type character: Character
        :param time_to_wait: amount of ticks to wait
        :type time_to_wait: int
        """
        super().__init__()

        self.action_type = 'wait'
        self.character = character
        self.time_to_wait = time_to_wait

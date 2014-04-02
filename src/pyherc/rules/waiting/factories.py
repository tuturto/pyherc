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
Wait related factories
"""
from pyherc.aspects import log_debug, log_info
from pyherc.rules.factory import SubActionFactory
from pyherc.rules.waiting.action import WaitAction


class WaitFactory(SubActionFactory):
    """
    Factory for creating wait actions

    .. versionadded:: 0.10
    """
    @log_debug
    def __init__(self):
        """
        Constructor for this factory
        """
        super().__init__()
        self.action_type = 'wait'

    @log_info
    def get_action(self, parameters):
        """
        Create a wait action

        :param parameters: parameters used to control creation
        :type parameters: WaitParameters
        """
        return WaitAction(character=parameters.character,
                          time_to_wait=parameters.time_to_wait)

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

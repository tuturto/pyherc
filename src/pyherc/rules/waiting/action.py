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
Module defining wait related actions
"""
from hymn.types.either import Left, Right
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
        if not self.is_legal():
            return Left(self.character)

        self.character.tick = self.character.tick + self.time_to_wait

        return Right(self.character)

    @log_debug
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if waiting is possible, false otherwise
        :rtype: Boolean
        """
        return True

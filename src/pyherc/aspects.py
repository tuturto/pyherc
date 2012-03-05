#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
Module for aspects
"""

from Aspyct.aop import Aspect
import logging

class Logged(Aspect):
    """
    Aspect to perform logging
    """
    def __init__(self, name):
        """
        Default constructor

        Args:
            name: Name of the logger
        """
        self.name = name
        self.logger = logging.getLogger(name)

    def atCall(self, call_data):
        """
        Called right before associated method is called
        """
        args = call_data.args
        kwargs = call_data.kwargs
        function = call_data.function

        log_message = '{0} :call: {1} : {2}'.format(function, args, kwargs)
        self.logger.debug(log_message)

    def atRaise(self, call_data):
        """
        Called when associated method raises an exception
        """
        pass

    def atReturn(self, call_data):
        """
        Called right after associated method returns
        """
        function = call_data.function
        return_value = call_data.returned

        log_message = '{0} :return: {1}'.format(function, return_value)
        self.logger.debug(log_message)


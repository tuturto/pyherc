#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
    def __init__(self):
        """
        Default constructor
        """
        self.logger = None

    def atCall(self, call_data):
        """
        Called right before associated method is called
        """
        args = call_data.args
        kwargs = call_data.kwargs
        function = call_data.function

        if self.logger == None:
            cls = call_data.cls
            if cls != None:
                logger_name = cls.__module__ + "." + cls.__name__
            else:
                logger_name = call_data.function.__name__

            self.logger = logging.getLogger(logger_name)

        if function != None:
            function_name = function.__name__
        else:
            function_name = ' '

        log_message = '{0} :call: {1} : {2}'.format(
                                                    function_name,
                                                    args,
                                                    kwargs)
        self.logger.debug(log_message)

    def atRaise(self, call_data):
        """
        Called when associated method raises an exception
        """
        function = call_data.function
        exception = call_data.exception

        if function != None:
            function_name = function.__name__
        else:
            function_name = ' '

        log_message = '{0} :exception raised: {1}'.format(
                                                          function_name,
                                                          exception)
        self.logger.error(log_message)

    def atReturn(self, call_data):
        """
        Called right after associated method returns
        """
        function = call_data.function
        return_value = call_data.returned

        if function != None:
            function_name = function.__name__
        else:
            function_name = ' '

        log_message = '{0} :return: {1}'.format(function_name,
                                                return_value)
        self.logger.debug(log_message)


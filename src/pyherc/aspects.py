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
Module for aspects
"""
import logging, sys
from decorator import decorator

def create_logger(log_level):

    @decorator
    def level_logger(wrapped_function, *args, **kwargs):
        """
        Decorator to perform logging
        """
        logger_name = str(wrapped_function)
        logger = logging.getLogger(logger_name)

        call_message = ' '.join([logger_name,
                                 'call',
                                 ':',
                                 str(args),
                                 str(kwargs)])

        logger.log(log_level, call_message)
    
        try:
            result = wrapped_function(*args, **kwargs)

            result_message = ' '.join([logger_name,
                                       'return',
                                       ':',
                                       str(result)])

            logger.log(log_level, result_message)

            return result
        except Exception as err:
            logger.critical(err)
            raise

    return level_logger

log_debug = create_logger(logging.DEBUG)

log_info = create_logger(logging.INFO)

log_warning = create_logger(logging.WARNING)

log_error = create_logger(logging.ERROR)

log_critical = create_logger(logging.CRITICAL)

def no_logger(wrapped_function):
    """
    Decorator to perform no logging at all
    """    
    return wrapped_function

def set_logger(log_level, silent):
    """
    Set application-wide log level
    """
    global log_debug
    global log_info
    global log_warning
    global log_error
    global log_critical
    
    if log_level == 'debug':
        pass
    elif log_level == 'info':
        log_debug = no_logger
    elif log_level == 'warning':
        log_debug = no_logger
        log_info = no_logger
    elif log_level == 'error':
        log_debug = no_logger
        log_info = no_logger
        log_warning = no_logger
    elif log_level == 'critical':
        log_debug = no_logger
        log_info = no_logger
        log_warning = no_logger
        log_error = no_logger
    else:
        assert False

    if silent:
        log_debug = no_logger
        log_info = no_logger
        log_warning = no_logger
        log_error = no_logger
        log_critical = no_logger

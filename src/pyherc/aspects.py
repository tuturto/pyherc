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
import logging
from functools import wraps
from decorator import decorator

@decorator
def logged(wrapped_function, *args, **kwargs):
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

    logger.debug(call_message)

    result = wrapped_function(*args, **kwargs)

    result_message = ' '.join([logger_name,
                                   'return',
                                   ':',
                                   str(result)])

    logger.debug(result_message)

    return result

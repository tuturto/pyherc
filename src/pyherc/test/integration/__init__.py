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
Package for tests that access hard drive
"""

import os.path

def detect_base_path():
    search_directory = '.'
    current = os.path.normpath(os.path.join(os.getcwd(), search_directory))

    while not os.path.exists(os.path.join(current, 'resources')):
        search_directory = search_directory +'/..'
        current = os.path.normpath(os.path.join(os.getcwd(),
                                                    search_directory))

    base_path = os.path.join(current, 'resources')

    return base_path

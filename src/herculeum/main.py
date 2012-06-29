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
Main entry point for Herculeum - game
"""
import sys
import os.path
import pygame
import thread

from pyherc.debug import get_debug_server
from pyherc.application import APP

INSTALL_PATH = os.path.abspath(".")
sys.path.append(INSTALL_PATH)


if not pygame.font:
    print 'Warning, fonts disabled'

if not pygame.mixer:
    print 'Warning, sound disabled'

print '#   pyherc is free software: you can redistribute it and/or modify'
print '#   it under the terms of the GNU General Public License as published by'
print '#   the Free Software Foundation, either version 3 of the License, or'
print '#   (at your option) any later version.'
print '#'
print '#   pyherc is distributed in the hope that it will be useful,'
print '#   but WITHOUT ANY WARRANTY; without even the implied warranty of'
print '#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the'
print '#   GNU General Public License for more details.'
print '#'
print '#   You should have received a copy of the GNU General Public License'
print '#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.'

if __name__ == "__main__":
    APP.detect_resource_directory()
    APP.process_command_line()
    APP.start_logging()
    APP.load_configuration()

    server = get_debug_server()
    if server != None:
        thread.start_new_thread(server.run, ())

    APP.run()


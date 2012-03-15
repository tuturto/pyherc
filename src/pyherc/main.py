#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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
Main entry point for pyherc - game
"""
import sys
import os.path
import pygame
import thread

try:
    import web
    web_loaded = True
except ImportError:
    web_loaded = False

INSTALL_PATH = os.path.abspath(".")
sys.path.append(INSTALL_PATH)

from pyherc.application import APP

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

class Index:
    def GET(self):
        return '''
        <html><head></head><body>
        <p><a href="map">Map</a></p>
        <p><a href="player">Player</a></p>
        </body></html>
        '''

class Map:
    def GET(self):
        return APP.world.player.level.dump_string()

class Player:
    def GET(self):
        data = vars(APP.world.player)
        return_value = ''

        for key in data.keys():
            return_value = return_value + key + " : " + str(data[key]) + '\n'

        return return_value

if __name__ == "__main__":
    if web_loaded == False:
        print 'web.py not found, debug server not available'
    else:
        urls = (
            '/', 'Index',
            '/map', 'Map',
            '/player', 'Player'
            )
        app = web.application(urls, globals())
        thread.start_new_thread(app.run, ())

    APP.detect_resource_directory()
    APP.process_command_line(sys.argv[1:])
    APP.start_logging()
    APP.load_configuration()
    APP.run()

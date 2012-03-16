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
Module for page handlers
"""
import pyherc
from pyherc.application import APP
from pyherc.debug.data import render

try:
    import web
except ImportError:
    pass

def initialise_server():
    pyherc.debug.data.render = web.template.render(
                                '{0}/html/'.format(APP.base_path))

def get_urls():
    return (
            '/', 'pyherc.debug.Index',
            '/map', 'pyherc.debug.Map',
            '/player', 'pyherc.debug.Player'
            )

class Index:
    def GET(self):
        return pyherc.debug.data.render.index()

class Map:
    def GET(self):
        return APP.world.player.level.dump_string()

class Player:
    def GET(self):
        return pyherc.debug.data.render.player(APP.world.player)


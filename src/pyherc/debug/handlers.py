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
    """
    Initialise render component for server
    """
    pyherc.debug.data.render = web.template.render(
                                '{0}/html/'.format(APP.base_path))

def get_urls():
    """
    Get mapping between urls and handlers

    Returns:
        Mapping that can be passed on web.application
    """
    return (
            '/', 'Index',
            '/map', 'Map',
            '/player', 'Player'
            )

def get_debug_server():
    """
    Set up debug server

    Returns:
        Initialised debug server
    """
    initialise_server()
    app = web.application(get_urls(), vars(pyherc.debug.handlers))
    return app

class Index:
    """
    Class for displaying start page
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def GET(self):
        """
        Handle http get
        """
        return pyherc.debug.data.render.index()

class Map:
    """
    Class for displaying map
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def GET(self):
        """
        Handle http get
        """
        return APP.world.player.level.dump_string()

class Player:
    """
    Class for displaying player
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def GET(self):
        """
        Handle http get
        """
        return pyherc.debug.data.render.player(APP.world.player)


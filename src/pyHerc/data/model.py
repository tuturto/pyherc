#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

import logging

class Model:
    """
    Represents playing world
    """

    def __init__(self):
        self.logger = logging.getLogger('pyHerc.data.model.Model')
        self.dungeon = None
        self.player = None
        self.config = None

        self.logger.info('loading config')
        self.loadConfig()
        self.logger.info('config loaded')

    def loadConfig(self):
        """
        Loads config
        """
        self.config = {}
        self.config['level'] = {}
        self.config['level']['size']  = (80,  30)

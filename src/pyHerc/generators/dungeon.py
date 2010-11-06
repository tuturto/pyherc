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

import os, sys
import logging

class DungeonGenerator:
    """
    This class is used to generate dungeon
    """

    def __init__(self):
        self.logger = logging.getLogger('pyHerc.generators.dungeon.DungeonGenerator')

    def generateDungeon(self):
        """
        Generates start of the dungeon
        """
        pass

class TestLevelGenerator:
    """
    Generates a simple test level
    """

    def generateLevel(self, stairs, model):
        """
        Generate level that starts from given stairs
        Will perform linking and required modifications to set up the model
        """
        pass

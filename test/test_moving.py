#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2009 Tuukka Turto
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

import pyHerc
from pyHerc.data.dungeon import Level
from pyHerc.data.dungeon import Dungeon
from pyHerc.data.model import Model
from pyHerc.data.model import Character
from pyHerc.generators.dungeon import TestLevelGenerator

import pyHerc.rules.moving

def test_simple_moving():
    """
    Test that taking single step is possible
    """
    model = Model()
    character = Character()
    generator = TestLevelGenerator()

    model.dungeon = Dungeon()
    generator.generateLevel(None, model)

    character.location = (5, 5)
    character.level = model.dungeon.levels

    assert(character.location == (5, 5))
    pyHerc.rules.moving.move(model, character, 3)
    assert(character.location == (6, 5))

def test_walking_to_walls():
    """
    Test that it is not possible to walk through walls
    """
    model = Model()
    character = Character()
    generator = TestLevelGenerator()

    model.dungeon = Dungeon()
    generator.generateLevel(None, model)

    character.location = (1, 1)
    character.level = model.dungeon.levels

    assert(character.location == (1, 1))
    pyHerc.rules.moving.move(model, character, 1)
    assert(character.location == (1, 1))

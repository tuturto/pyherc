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

import pyHerc
import pyHerc.generators.item
import pyHerc.data.tiles
import pyHerc.data.dungeon
import pyHerc.rules.items

def test_crystalSkullGeneration():
    """
    Test that generating crystal skull is possible
    """
    generator = pyHerc.generators.item.ItemGenerator()

    item = generator.generateItem({'type': 'special',
                                                'name': 'crystal skull'})

    assert(item.name == 'Crystal skull')
    assert(item.questItem == 1)
    assert(item.icon == pyHerc.data.tiles.item_crystal_skull)

def test_pickingUp():
    """
    Test that item can be picked up
    """
    item = pyHerc.data.model.Item()
    item.name = 'banana'
    item.location = ()
    item.icon = None

    level = pyHerc.data.dungeon.Level([20, 20], pyHerc.data.tiles.floor_rock,
                                                    pyHerc.data.tiles.wall_empty)

    character = pyHerc.data.model.Character()

    character.location = (5, 5)
    character.name = 'Timothy Tester'
    character.level = level

    level.addItem(item, (5, 5))

    dungeon = pyHerc.data.dungeon.Dungeon()
    dungeon.levels = level

    model = pyHerc.data.model.Model()
    model.dungeon = dungeon
    model.player = character

    pyHerc.rules.items.pickUp(model, character, item)

    assert(item in character.inventory)
    assert(not item in level.items)

def test_pickingUpNotCorrectLocation():
    """
    Test that item is not picked up from wrong location
    """
    item = pyHerc.data.model.Item()
    item.name = 'banana'
    item.location = ()
    item.icon = None

    level = pyHerc.data.dungeon.Level([20, 20], pyHerc.data.tiles.floor_rock,
                                                    pyHerc.data.tiles.wall_empty)

    character = pyHerc.data.model.Character()

    character.location = (6, 6)
    character.name = 'Timothy Tester'
    character.level = level

    level.addItem(item, (5, 5))

    dungeon = pyHerc.data.dungeon.Dungeon()
    dungeon.levels = level

    model = pyHerc.data.model.Model()
    model.dungeon = dungeon
    model.player = character

    pyHerc.rules.items.pickUp(model, character, item)

    assert(not item in character.inventory)
    assert(item in level.items)

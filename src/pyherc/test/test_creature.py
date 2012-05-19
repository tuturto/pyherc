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
#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

"""
Module for testing creatures
"""
#pylint: disable=W0614
from pyherc.data import WeaponProficiency
from pyherc.test import IntegrationTest
from pyherc.test.builders import CharacterBuilder
from pyherc.test.builders import ItemBuilder
from pyherc.generators.level.testlevel import TestLevelGenerator
from pyherc.data.dungeon import Dungeon
from pyherc.rules.moving import deactivate
from hamcrest import * #pylint: disable=W0401

class TestCreatureWithGenerator(IntegrationTest):
    """
    Tests for creatures that require generators to be working
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestCreatureWithGenerator, self).__init__()

    def test_rat_generation(self):
        """
        Test that generating a rat is possible
        """
        creature = self.creatureGenerator.generate_creature({'name': 'rat'})

        assert_that(creature.name, is_(equal_to('rat')))

    def test_is_proficient(self):
        """
        Test that weapon proficiency of character can be checked
        """
        creature = CharacterBuilder().build()

        weapon = self.item_generator.generate_item({'name' : 'club'})

        proficiency = creature.is_proficient(weapon)
        assert_that(proficiency, is_(equal_to(False)))

        creature.feats.append(WeaponProficiency('simple'))

        proficiency = creature.is_proficient(weapon)
        assert_that(proficiency, is_(equal_to(True)))

class TestStatues(IntegrationTest):
    """
    Test handling of statues (mainly mimicing items)
    """

    def __init__(self):
        """
        Default constructor
        """
        super(TestStatues, self).__init__()

    def test_deactivating_creature(self):
        """
        Test that activated character can deactivate
        """
        creature = (CharacterBuilder()
                        .with_model(self.model)
                        .with_action_factory(self.action_factory)
                        .with_rng(self.rng)
                        .with_name('Mimic')
                        .build())

        item = (ItemBuilder()
                    .with_name('Chest')
                    .build())

        creature.set_mimic_item(item)

        levelGenerator = TestLevelGenerator(self.action_factory,
                                            self.creatureGenerator,
                                            self.item_generator)

        self.model.dungeon = Dungeon()
        self.level1 = levelGenerator.generate_level(None, self.model, monster_list = [])

        self.model.dungeon.levels = self.level1

        self.level1.add_creature(creature, self.level1.find_free_space())

        location = creature.location

        creatures = self.level1.get_creature_at(location)
        items = self.level1.get_items_at(location)
        assert_that(creatures, is_(same_instance(creature)))
        assert_that(len(items), is_(equal_to(0)))

        deactivate(self.model, creature)

        creatures = self.level1.get_creature_at(location)
        items = self.level1.get_items_at(location)
        assert_that(creatures, is_(none()))
        assert_that(len(items), is_(equal_to(1)))

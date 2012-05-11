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
Module for testing poison related rules
"""
#pylint: disable=W0614
from pyherc.rules.effects import Poison
from pyherc.rules.effects import EffectsFactory
from pyherc.test.builders import CharacterBuilder
from pyherc.test.builders import LevelBuilder
from pyherc.test.matchers import has_active_effect, is_not_at
from mockito import mock
from hamcrest import * #pylint: disable=W0401

class TestPoison():
    """
    Basic tests for poison
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_cause_damage(self):
        """
        Test that triggered poison will damage character
        """
        character = (CharacterBuilder()
                        .with_hit_points(10)
                        .build())

        poison = Poison(duration = 1,
                        frequency = 1,
                        tick = 0,
                        damage = 5,
                        target = character)

        poison.trigger()

        assert_that(character.hit_points, is_(equal_to(5)))

    def test_character_can_die(self):
        """
        Test that character with less than 1 hit points is removed from play
        """
        character = (CharacterBuilder()
                        .with_hit_points(5)
                        .build())

        level = (LevelBuilder()
                    .with_character(character)
                    .build())

        poison = Poison(duration = 0,
                        frequency = 0,
                        tick = 0,
                        damage = 10,
                        target = character)

        poison.trigger()

        assert_that(character, is_not_at(level))

class TestEffectsFactory():
    """
    Poison related tests for effects factory
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_creating_poison(self):
        """
        Test that poison effect can be created
        """
        character = CharacterBuilder().build()
        factory = EffectsFactory()
        factory.add_effect('poison',
                            {'type': Poison,
                            'duration': 150,
                            'frequency': 30,
                            'tick': 10,
                            'damage': 5})

        effect = factory.create_effect('poison',
                                       target = character)

        assert_that(effect.duration, is_(equal_to(150)))
        assert_that(effect.frequency, is_(equal_to(30)))
        assert_that(effect.damage, is_(equal_to(5)))
        assert_that(effect.target, is_(equal_to(character)))

    def test_creating_poison_with_paramarray(self):
        """
        Test that poison can be created by passing it a parameter array
        """
        character = CharacterBuilder().build()

        params = {'duration': 150,
                  'frequency': 30,
                  'tick': 10,
                  'damage': 1,
                  'target': character}

        effect = Poison(**params)

        assert_that(effect.duration, is_(equal_to(150)))
        assert_that(effect.frequency, is_(equal_to(30)))
        assert_that(effect.damage, is_(equal_to(1)))
        assert_that(effect.target, is_(equal_to(character)))

class TestCharacter():
    """
    Test Character methods related to poison
    """
    def __init__(self):
        """
        Default constructor
        """

    def test_adding_effect(self):
        """
        Test that poison effect can be added to a character
        """
        character = CharacterBuilder().build()
        poison = mock(Poison)

        character.add_effect(poison)

        assert_that(character, has_active_effect(poison))

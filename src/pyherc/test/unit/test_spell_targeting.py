# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
Tests for spell targeting
"""
from hamcrest import (assert_that, contains_inanyorder, has_length, is_, is_in,
                      is_not)
from pyherc.generators.spells import (targeting_single_target,
                                      targeting_spherical_area)
from pyherc.rules.magic.interface import SpellCastingParameters
from pyherc.test.builders import CharacterBuilder, LevelBuilder
from pyherc.test.matchers import void_target_at, wall_target_at
from pyherc.data import wall_tile

FLOOR = 1
SOLID_WALL = 2
EMPTY_WALL = None

class TestSingleCharacterTargeting():
    """
    Tests for targeting a single character
    """

    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.level = None
        self.caster = None
        self.target1 = None

    def setup(self):
        """
        Setup test cases
        """
        self.caster = (CharacterBuilder()
                           .with_name('Carth the Caster')
                           .build())

        self.target1 = (CharacterBuilder()
                            .with_name('Tammy the Target1')
                            .build())

        self.level = (LevelBuilder()
                          .with_character(self.caster, (10, 5))
                          .with_character(self.target1, (5, 5))
                          .with_floor_tile(FLOOR)
                          .with_wall_tile(EMPTY_WALL)
                          .with_empty_wall_tile(EMPTY_WALL)
                          .with_solid_wall_tile(SOLID_WALL)
                          .build())

    def test_targeting_correct_direction(self):
        """
        When targeting towards character, a spell should hit
        """
        params = SpellCastingParameters(caster = self.caster,
                                        direction = 7,
                                        spell_name = 'proto')

        targets = [data.target for data in targeting_single_target(params)]

        assert_that(self.target1, is_in(targets))

    def test_targeting_empty_direction(self):
        """
        Targeting to incorrect direction should not add anyone to targets list
        """
        params = SpellCastingParameters(caster = self.caster,
                                        direction = 1,
                                        spell_name = 'proto')

        targets = targeting_single_target(params)

        assert_that(self.target1, is_not(is_in(targets)))

    def test_caster_is_not_targeted(self):
        """
        Under no circumstances, caster should not be targeted
        """
        params = SpellCastingParameters(caster = self.caster,
                                        direction = 7,
                                        spell_name = 'proto')

        targets = targeting_single_target(params)

        assert_that(self.caster, is_not(is_in(targets)))

    def test_targeting_wall(self):
        """
        When targeting wall, it should be reported
        """
        self.level.walls[10][20] = SOLID_WALL

        params = SpellCastingParameters(caster = self.caster,
                                        direction = 5,
                                        spell_name = 'proto')

        targets = targeting_single_target(params)
        target = targets[0]

        assert_that(target, is_(wall_target_at((10, 20))))

    def test_retrieving_previous_tile(self):
        """
        When reporting target, the previous tile should be reported too
        """
        wall_tile(self.level (10, 20), SOLID_WALL)

        params = SpellCastingParameters(caster = self.caster,
                                        direction = 5,
                                        spell_name = 'proto')

        targets = targeting_single_target(params)
        target = targets[0].previous_target

        assert_that(target, is_(void_target_at((10, 19))))


class TestSphericalAreaTargetting():
    """
    Tests for targeting spherical area
    """

    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.caster = None
        self.target1 = None
        self.target2 = None
        self.target3 = None

    def setup(self):
        """
        Setup test cases
        """
        self.caster = (CharacterBuilder()
                           .with_name('Carth the Caster')
                           .build())

        self.target1 = (CharacterBuilder()
                            .with_name('Tammy the Target1')
                            .build())
        self.target2 = (CharacterBuilder()
                            .with_name('Tim the Target2')
                            .build())
        self.target3 = (CharacterBuilder()
                            .with_name('Tebathine the Target3')
                            .build())

        self.level = (LevelBuilder()
                          .with_character(self.caster, (15, 5))
                          .with_character(self.target1, (5, 5))
                          .with_character(self.target2, (5, 6))
                          .with_floor_tile(FLOOR)
                          .with_wall_tile(EMPTY_WALL)
                          .with_empty_wall_tile(EMPTY_WALL)
                          .with_solid_wall_tile(SOLID_WALL)
                          .build())

    def test_area_effect_is_calculated(self):
        """
        Spells with area effect should be able to target multiple targets
        """
        params = SpellCastingParameters(caster = self.caster,
                                        direction = 7,
                                        spell_name = 'proto')

        data = targeting_spherical_area(params,
                                        radius = 2)
        targets = [x.target for x in data
                   if x.target]

        assert_that(targets, contains_inanyorder(self.target1,
                                                 self.target2))

    def test_corners_are_rounded(self):
        """
        Spells with spherical area of effect should not target to square area
        """
        self.level.add_creature(self.target3,
                                (7, 7))

        params = SpellCastingParameters(caster = self.caster,
                                        direction = 7,
                                        spell_name = 'proto')

        targets = targeting_spherical_area(params,
                                           radius = 2)

        assert_that(self.target3, is_not(is_in(targets)))

    def test_splash_does_not_penetrate_walls(self):
        """
        In normal situations, splash should be stopped by walls
        """
        wall_tile(self.level (6, 4), SOLID_WALL)
        wall_tile(self.level (6, 5), SOLID_WALL)
        wall_tile(self.level (6, 6), SOLID_WALL)

        params = SpellCastingParameters(caster = self.caster,
                                        direction = 7,
                                        spell_name = 'proto')

        data = targeting_spherical_area(params,
                                        radius = 6)

        targets = [x.target for x in data
                   if x.target]

        assert_that(targets, has_length(0))

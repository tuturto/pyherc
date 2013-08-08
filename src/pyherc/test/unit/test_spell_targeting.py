# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
from pyherc.test.builders import LevelBuilder, CharacterBuilder
from pyherc.generators.spells import targeting_single_target
from pyherc.rules import SpellCastingParameters
from hamcrest import assert_that, is_in, is_not

class TestSingleCharacterTargeting():
    """
    Tests for targeting a single character
    """

    def __init__(self):
        """
        Default constructor
        """
        super(TestSingleCharacterTargeting, self).__init__()

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
                          .build())

    def test_targeting_correct_direction(self):
        """
        When targeting towards character, a spell should hit
        """
        params = SpellCastingParameters(caster = self.caster,
                                        direction = 7,
                                        spell_name = 'proto')

        targets = targeting_single_target(params)

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

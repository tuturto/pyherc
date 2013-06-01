#!/usr/bin/env python3
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
Tests for magical spells
"""

from pyherc.test.builders import LevelBuilder, CharacterBuilder
from pyherc.test.builders import SpellGeneratorBuilder

from hamcrest import assert_that, is_in

class TestTargetingSingle():
    """
    Tests for spells targeting single character
    """
    def __init__(self):
        """
        Default constructor
        """
        pass
    
    def test_target_single(self):
        """
        Targeting a single character should be possible
        """
        level = LevelBuilder().build()
        
        character = (CharacterBuilder()
                        .with_level(level)
                        .with_location((5, 5))
                        .build())

        spell_generator = SpellGeneratorBuilder().build()

        spell = spell_generator.create_spell(spell_name = 'healing wind', 
                                             target = character)

        assert_that(character, is_in(spell.target))
        

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
from pyherc.test.builders import SpellGeneratorBuilder, SpellBuilder
from pyherc.generators import EffectsFactory
from pyherc.data.effects import EffectHandle, Effect
from pyherc.rules.ending import Dying

from hamcrest import assert_that, is_in #pylint: disable-msg=E0611
from mockito import mock, verify, when

class TestSpellTargetingSingle():
    """
    Tests for spells targeting single character
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.character = None
        self.spell_generator = None

    def setup(self):
        """
        Setup test cases
        """
        self.level = LevelBuilder().build()

        self.character = (CharacterBuilder()
                                .with_level(self.level)
                                .with_location((5, 5))
                                .build())

        self.spell_generator = SpellGeneratorBuilder().build()

    def test_target_single(self):
        """
        Targeting a single character should be possible
        """
        spell = self.spell_generator.create_spell(spell_name = 'healing wind',
                                                  target = self.character)

        assert_that(self.character, is_in(spell.target))

class TestSpellEffects():
    """
    Tests for spell effects
    """

    def __init__(self):
        """
        Default constructor
        """
        self.effects_factory = None
        self.effect = None
        self.dying_rules = None
        self.effect_handle = None
        self.spell = None

    def setup(self):
        """
        Setup test cases
        """
        self.character = (CharacterBuilder()
                                .build())

        self.effects_factory = mock(EffectsFactory)
        self.effect = mock(Effect)
        self.dying_rules = mock(Dying)
        when(self.effects_factory).create_effect(key = 'healing wind',
                                            target = self.character).thenReturn(self.effect)

        self.effect_handle = EffectHandle(trigger = 'on spell hit',
                                          effect = 'healing wind',
                                          parameters = {},
                                          charges = 1)

        self.spell = (SpellBuilder()
                        .with_effect_handle(self.effect_handle)
                        .with_target(self.character)
                        .build())

    def test_creating_effect(self):
        """
        Casting a spell should create effects it has
        """
        self.spell.cast(self.effects_factory,
                        self.dying_rules)

        verify(self.effects_factory).create_effect(key = 'healing wind',
                                                   target = self.character)

    def test_triggering_effect(self):
        """
        Casting a spell should trigger the effect
        """
        self.spell.cast(self.effects_factory, 
                        self.dying_rules)
        
        verify(self.effect).trigger(self.dying_rules)

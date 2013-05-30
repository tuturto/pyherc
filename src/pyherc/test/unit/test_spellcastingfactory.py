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
Module for SpellCastingFactory related tests
"""
from pyherc.rules import SpellCastingParameters

from pyherc.test.builders import ActionFactoryBuilder, SpellGeneratorBuilder
from pyherc.test.builders import SpellCastingFactoryBuilder

from mockito import mock, when, verify
from hamcrest import assert_that, is_not #pylint: disable-msg=E0611

class TestSpellCastingFactory:
    """
    Tests for magic
    """

    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_creating_action(self):
        """
        Test that action can be created
        """
        action_factory = (ActionFactoryBuilder()
                                    .with_spellcasting_factory()
                                    .build())
        
        action = action_factory.get_action(
                                           SpellCastingParameters(self,
                                                                  direction = 1, 
                                                                  spell_name = 'healing wind'))
        
        assert_that(action, is_not(None))

    def test_spell_is_created_with_a_factory(self):
        """
        When creating a spell casting action, spell should be created
        """
        spell_factory = SpellGeneratorBuilder().build()
        when(spell_factory).create_spell('healing wind').thenReturn(mock())
        spellcasting_factory = (SpellCastingFactoryBuilder()
                                            .with_spell_factory(spell_factory)
                                            .build())
        
        spellcasting_factory.get_action(
                                  SpellCastingParameters(self,
                                                                  direction = 1, 
                                                                  spell_name = 'healing wind'))
        
        verify(spell_factory).create_spell('healing wind')

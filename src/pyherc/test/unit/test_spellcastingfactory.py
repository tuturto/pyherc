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
Module for SpellCastingFactory related tests
"""
from hamcrest import assert_that, is_not  # pylint: disable-msg=E0611
from mockito import any, mock, verify, when
from pyherc.rules.magic.interface import SpellCastingParameters
from pyherc.test.builders import (ActionFactoryBuilder, EffectsFactoryBuilder,
                                  SpellCastingFactoryBuilder,
                                  SpellGeneratorBuilder)


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
        spell_factory = mock()
        when(spell_factory).build().thenReturn(spell_factory)
        when(spell_factory).create_spell(any(), any()).thenReturn([mock()])
        spell_factory.spell_list = {'healing wind': mock()}
        action_factory = (ActionFactoryBuilder()
                                    .with_spellcasting_factory(
                                        SpellCastingFactoryBuilder()
                                            .with_spell_factory(spell_factory)
                                            .build())
                                    .build())

        action = action_factory.get_action(SpellCastingParameters(self,
                                                                  direction = 1,
                                                                  spell_name = 'healing wind'))

        assert_that(action, is_not(None))

    def test_spell_is_created_with_a_factory(self):
        """
        When creating a spell casting action, spell should be created
        """
        caster = mock()
        spell_factory = SpellGeneratorBuilder().build()
        effects_factory = EffectsFactoryBuilder().build()
        when(spell_factory).create_spell('healing wind').thenReturn(mock())  #pylint: disable-msg=E1103
        spellcasting_factory = (SpellCastingFactoryBuilder()
                                            .with_spell_factory(spell_factory)
                                            .with_effects_factory(effects_factory)
                                            .build())

        spellcasting_factory.get_action(
                                  SpellCastingParameters(caster,
                                                         direction = 1,
                                                         spell_name = 'healing wind'))

        verify(spell_factory).create_spell(spell_name = 'healing wind',
                                           targets = any())

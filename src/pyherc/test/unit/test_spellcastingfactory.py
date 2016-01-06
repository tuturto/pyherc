# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for SpellCastingFactory related tests
"""
from hamcrest import assert_that, is_not  # pylint: disable-msg=E0611
from mockito import any, mock, verify, when
from pyherc.ports.magic import SpellCastingParameters
from pyherc.test.builders import (ActionFactoryBuilder,
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

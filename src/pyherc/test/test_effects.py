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
Module for testing effects
"""

#pylint: disable=W0614
from pyherc.data import Character, Item, ItemEffectData
from pyherc.rules.effects import Heal
from pyherc.rules.effects import Poison
from pyherc.rules.effects import EffectsFactory
from random import Random
from mockito import mock, when
from hamcrest import * #pylint: disable=W0401

class TestEffects(object):
    """
    """
    pass

    def test_create_effect_while_drinking(self):
        """
        Test that effect will be created when drinking potion
        """
        effect_spec = mock(ItemEffectData)
        potion = mock(Item)

        when(potion).get_effects('on drink').thenReturn(effect_spec)

        character = mock(Character)
        character.drink(potion)

        # verify(potion).trigger()


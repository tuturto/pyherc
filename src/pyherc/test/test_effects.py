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
from pyherc.rules.effects import Effect
from pyherc.rules.effects import EffectsFactory
from pyherc.rules.effects import EffectsConfiguration
from pyherc.rules.public import ActionFactory
from pyherc.rules.consume.factories import DrinkFactory
from random import Random

from mockito import mock, when, any, verify
from hamcrest import * #pylint: disable=W0401

class TestEffects(object):
    """
    Tests for effects in general
    """

    def test_effect_triggered_while_drinking(self):
        """
        Test that effect will be triggered when drinking potion
        """
        effect_factory = mock(EffectsFactory)
        effect_spec = mock(ItemEffectData)
        effect = mock (Effect)
        potion = mock(Item)

        effect_spec.charges = 2
        when(potion).get_effects('on drink').thenReturn([effect_spec])
        when(effect_factory).create_effect(any()).thenReturn(effect)

        model = mock()
        action_factory = ActionFactory(model = model,
                                       factories = [DrinkFactory(effect_factory)])

        character = Character(model = model,
                              action_factory = action_factory,
                              rng = Random())
        character.drink(potion)

        verify(effect).trigger()

    def test_creating_effect(self):
        """
        Test that effect can be created
        """
        effects_configuration = EffectsConfiguration()

        effects_configuration.add_configuration(
                            'major heal',
                            {'duration': 10,
                            'frequency': 2,
                            'tick': 2,
                            'healing': 4})

        effect_factory = EffectsFactory(effects_configuration)
        effect_factory.add_effect('major heal', Heal)

        potion = Item()
        potion.add_effect(ItemEffectData(trigger = 'on drink',
                                         effect = 'major heal',
                                         parameters = None,
                                         charges = 2))

        action_factory = ActionFactory(model = mock(),
                                       factories = [DrinkFactory(effect_factory)])

        character = Character(model = mock(),
                              action_factory = action_factory,
                              rng = Random())
        character.hit_points = 1
        character.max_hp = 10
        character.drink(potion)

        assert_that(character.hit_points, is_(equal_to(10)))

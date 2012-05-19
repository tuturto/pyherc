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
from pyherc.rules.effects import Heal
from pyherc.rules.effects import Poison
from pyherc.rules.effects import Effect
from pyherc.rules.effects import EffectsFactory
from pyherc.rules.effects import EffectHandle
from pyherc.rules.public import ActionFactory
from pyherc.rules.consume.factories import DrinkFactory
from random import Random
from pyherc.test.builders import CharacterBuilder, ItemBuilder
from pyherc.test.builders import EffectHandleBuilder, ActionFactoryBuilder
from pyherc.test.builders import LevelBuilder
from pyherc.test.matchers import has_active_effects, has_no_active_effects

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
        effect_spec = mock(EffectHandle)
        effect = mock (Effect)
        effect.duration = 0
        potion = mock()

        effect_spec.charges = 2
        when(potion).get_effect_handles('on drink').thenReturn([effect_spec])
        when(effect_factory).create_effect(any(),
                                           target = any()).thenReturn(effect)

        model = mock()
        action_factory = ActionFactory(model = model,
                                       factories = [DrinkFactory(effect_factory)])

        character = (CharacterBuilder()
                        .with_model(model)
                        .with_action_factory(action_factory)
                        .build())
        character.drink(potion)

        verify(effect).trigger()

    def test_effect__triggered_when_hitting_target(self):
        """
        Test that effect is triggered when attack hits target
        """
        effect = mock()
        effect.duration = 0
        model = mock()

        effect_factory = mock(EffectsFactory)
        when(effect_factory).create_effect(any(),
                                           target = any()).thenReturn(effect)

        action_factory = (ActionFactoryBuilder()
                            .with_model(model)
                            .with_attack_factory()
                            .with_effect_factory(effect_factory)
                            .build())

        attacker = (CharacterBuilder()
                        .with_effect(
                                EffectHandleBuilder()
                                    .with_trigger('on attack hit'))
                        .with_action_factory(action_factory)
                        .with_location((5, 5))
                        .build())

        defender = (CharacterBuilder()
                        .with_location((6, 5))
                        .build())

        level = (LevelBuilder()
                    .with_character(attacker)
                    .with_character(defender)
                    .build())

        attacker.perform_attack(3)

        verify(effect).trigger()

    def test_creating_effect(self):
        """
        Test that effect can be created and triggered immediately
        """
        effect_factory = EffectsFactory()
        effect_factory.add_effect(
                            'major heal',
                            {'type': Heal,
                            'duration': 0,
                            'frequency': 0,
                            'tick': 0,
                            'healing': 10})

        potion = (ItemBuilder()
                        .with_effect(
                            EffectHandleBuilder()
                                .with_trigger('on drink')
                                .with_effect('major heal')
                                .with_charges(2))
                        .build())

        action_factory = ActionFactory(model = mock(),
                                       factories = [DrinkFactory(effect_factory)])

        character = (CharacterBuilder()
                        .with_action_factory(action_factory)
                        .with_hit_points(1)
                        .with_max_hp(10)
                        .build())

        character.drink(potion)

        assert_that(character.hit_points, is_(equal_to(10)))
        assert_that(character, has_no_active_effects())

    def test_timed_effect_is_triggered(self):
        """
        Test that timed effect is triggered only after enough time
        has passed
        """
        effect_factory = EffectsFactory()
        effect_factory.add_effect(
                            'major heal',
                            {'type': Heal,
                            'duration': 12,
                            'frequency': 3,
                            'tick': 3,
                            'healing': 10})

        potion = (ItemBuilder()
                        .with_effect(
                            EffectHandleBuilder()
                                .with_trigger('on drink')
                                .with_effect('major heal')
                                .with_charges(2))
                        .build())

        action_factory = ActionFactory(model = mock(),
                                       factories = [DrinkFactory(effect_factory)])

        character = (CharacterBuilder()
                        .with_action_factory(action_factory)
                        .with_hit_points(1)
                        .with_max_hp(10)
                        .build())

        character.drink(potion)

        assert_that(character, has_active_effects(1))

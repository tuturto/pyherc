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
Module for testing effects
"""

from pyherc.data.effects import Heal
from pyherc.data.effects import Poison
from pyherc.data.effects import Effect
from pyherc.data import Model
from pyherc.generators import EffectsFactory
from pyherc.data.effects import EffectHandle
from pyherc.rules.combat.action import AttackAction
from pyherc.rules import drink
from pyherc.data.geometry import TargetData
from pyherc.rules import attack

from pyherc.events import PoisonAddedEvent
from pyherc.test.builders import CharacterBuilder, ItemBuilder
from pyherc.test.builders import EffectHandleBuilder, ActionFactoryBuilder
from pyherc.test.builders import DrinkFactoryBuilder
from pyherc.test.builders import EffectBuilder
from pyherc.test.builders import LevelBuilder
from pyherc.test.matchers import has_effect, has_effects, has_no_effects
from pyherc.test.matchers import EventType

from mockito import mock, when, any, verify, never
from hamcrest import assert_that, is_, equal_to, is_not


class TestEffects():
    """
    Tests for effects in general
    """

    def test_effect_triggered_while_drinking(self):
        """
        Test that effect will be triggered when drinking potion
        """
        effect_factory = mock(EffectsFactory)
        effect_spec = mock(EffectHandle)
        effect = mock(Effect)
        effect.duration = 0
        potion = mock()

        effect_spec.charges = 2
        when(potion).get_effect_handles('on drink').thenReturn([effect_spec])
        potion.maximum_charges_left = 2
        when(effect_factory).create_effect(any(),
                                           target=any()).thenReturn(effect)

        model = mock()
        action_factory = (ActionFactoryBuilder()
                          .with_model(model)
                          .with_drink_factory(DrinkFactoryBuilder()
                                              .with_effect_factory(effect_factory))  # noqa
                          .build())

        character = (CharacterBuilder()
                     .with_model(model)
                     .build())
        drink(character,
              potion,
              action_factory)

        verify(effect).trigger(any())

    def test_effect__triggered_when_hitting_target(self):
        """
        Test that effect is triggered when attack hits target
        """
        effect = mock()
        effect.duration = 0
        model = mock()
        rng = mock()

        when(rng).randint(1, 6).thenReturn(1)

        effect_factory = mock(EffectsFactory)
        when(effect_factory).create_effect(any(),
                                           target=any()).thenReturn(effect)

        action_factory = (ActionFactoryBuilder()
                          .with_model(model)
                          .with_attack_factory()
                          .with_effect_factory(effect_factory)
                          .build())

        attacker = (CharacterBuilder()
                    .with_effect_handle(EffectHandleBuilder()
                                        .with_trigger('on attack hit'))
                    .with_location((5, 5))
                    .build())

        defender = (CharacterBuilder()
                    .with_location((6, 5))
                    .build())

        (LevelBuilder().with_character(attacker)
                       .with_character(defender)
                       .build())

        attack(attacker,
               3,
               action_factory,
               rng)

        verify(effect).trigger(any())

    def test_effect_on_weapon_triggered_on_hit(self):
        """
        Effects on weapon should be triggered when landing a hit
        """
        effect = mock()
        effect.duration = 0
        model = mock()
        rng = mock()

        when(rng).randint(1, 6).thenReturn(1)

        effect_factory = mock(EffectsFactory)
        when(effect_factory).create_effect(any(),
                                           target=any()).thenReturn(effect)

        action_factory = (ActionFactoryBuilder()
                          .with_model(model)
                          .with_attack_factory()
                          .with_effect_factory(effect_factory)
                          .build())

        attacker = (CharacterBuilder()
                    .with_weapon(ItemBuilder()
                                 .with_damage(2, 'piercing')
                                 .with_effect(EffectHandleBuilder()
                                              .with_trigger('on attack hit')))
                    .with_location((5, 5))
                    .build())

        defender = (CharacterBuilder()
                    .with_location((6, 5))
                    .build())

        (LevelBuilder().with_character(attacker)
                       .with_character(defender)
                       .build())

        attack(attacker,
               3,
               action_factory,
               rng)

        verify(effect).trigger(any())

    def test_creating_effect(self):
        """
        Test that effect can be created and triggered immediately
        """
        effect_factory = EffectsFactory()
        effect_factory.add_effect('major heal',
                                  {'type': Heal,
                                   'duration': 0,
                                   'frequency': 0,
                                   'tick': 0,
                                   'healing': 10,
                                   'icon': 101,
                                   'title': 'title',
                                   'description': 'major heal'})

        potion = (ItemBuilder()
                  .with_effect(EffectHandleBuilder()
                               .with_trigger('on drink')
                               .with_effect('major heal')
                               .with_charges(2))
                  .build())

        action_factory = (ActionFactoryBuilder()
                          .with_drink_factory(DrinkFactoryBuilder()
                                              .with_effect_factory(effect_factory))  # noqa
                         .build())

        character = (CharacterBuilder()
                     .with_hit_points(1)
                     .with_max_hp(10)
                     .build())

        drink(character,
              potion,
              action_factory)

        assert_that(character.hit_points, is_(equal_to(10)))
        assert_that(character, has_no_effects())

    def test_timed_effect_is_triggered(self):
        """
        Test that timed effect is triggered only after enough time
        has passed
        """
        effect_factory = EffectsFactory()
        effect_factory.add_effect('major heal',
                                  {'type': Heal,
                                   'duration': 12,
                                   'frequency': 3,
                                   'tick': 3,
                                   'healing': 10,
                                   'icon': 100,
                                   'title': 'healig',
                                   'description': 'healing'})

        potion = (ItemBuilder()
                  .with_effect(EffectHandleBuilder()
                               .with_trigger('on drink')
                               .with_effect('major heal')
                               .with_charges(2))
                  .build())

        action_factory = (ActionFactoryBuilder()
                          .with_drink_factory(DrinkFactoryBuilder()
                                              .with_effect_factory(effect_factory))  # noqa
                            .build())

        character = (CharacterBuilder()
                     .with_hit_points(1)
                     .with_max_hp(10)
                     .build())

        drink(character,
              potion,
              action_factory)

        assert_that(character, has_effects(1))

    def test_effect_expiration_event_is_raised(self):
        """
        Test that effect expiration raises an event
        """
        model = mock()

        character = (CharacterBuilder()
                     .with_effect(EffectBuilder()
                                  .with_duration(0)
                                  .with_tick(10)
                                  .with_frequency(10))
                     .with_model(model)
                     .build())

        character.remove_expired_effects()

        verify(model).raise_event(EventType('remove event'))


class TestEffectsInMelee():
    """
    Test of effect creation and handling in melee
    """

    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.attacker = None
        self.defender = None
        self.model = None
        self.action_factory = None

    def setup(self):
        """
        Setup test case
        """
        self.model = mock()

        effect_factory = EffectsFactory()
        effect_factory.add_effect('poison',
                                  {'type': Poison,
                                   'duration': 12,
                                   'frequency': 3,
                                   'tick': 3,
                                   'damage': 5,
                                   'icon': 101,
                                   'title': 'poison',
                                   'description': 'Causes damage'})

        self.action_factory = (ActionFactoryBuilder()
                               .with_attack_factory()
                               .with_effect_factory(effect_factory)
                               .build())

        self.attacker = (CharacterBuilder()
                         .with_location((5, 5))
                         .with_effect_handle(EffectHandleBuilder()
                                             .with_trigger('on attack hit')
                                             .with_effect('poison'))
                         .with_model(self.model)
                         .build())

        self.defender = (CharacterBuilder()
                         .with_location((5, 4))
                         .with_hit_points(50)
                         .with_model(self.model)
                         .build())

        (LevelBuilder().with_character(self.attacker)
                       .with_character(self.defender)
                       .build())

    def test_add_effect_in_melee(self):
        """
        Test that effect can be added as a result of unarmed combat
        """
        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        attack(self.attacker,
               1,
               self.action_factory,
               rng)

        assert_that(self.defender, has_effect())

    def test_effects_do_not_stack(self):
        """
        Test that single type of effect will not added twice
        """
        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        attack(self.attacker,
               1,
               self.action_factory,
               rng)
        attack(self.attacker,
               1,
               self.action_factory,
               rng)

        assert_that(self.defender, has_effects(1))

    def test_effect_creation_event_is_raised(self):
        """
        Test that event is raised to indicate an effect was created
        """
        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        attack(self.attacker,
               1,
               self.action_factory,
               rng)

        verify(self.model).raise_event(any(PoisonAddedEvent))


class TestEffectHandling():
    """
    Test for adding effects
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.character = None

    def setup(self):
        """
        Setup test case
        """
        self.character = CharacterBuilder().build()

    def test_add_effect(self):
        """
        Adding a single effect should be possible
        """
        effect = EffectBuilder().build()

        self.character.add_effect(effect)

        assert_that(self.character, has_effect(effect))

    def test_add_multiple_effects(self):
        """
        It should be possible to add multiple effects of different type
        """
        effect_1 = (EffectBuilder()
                    .with_effect_name('spell')
                    .build())
        effect_2 = (EffectBuilder()
                    .with_effect_name('curse')
                    .build())

        self.character.add_effect(effect_1)
        self.character.add_effect(effect_2)

        assert_that(self.character, has_effect(effect_1))
        assert_that(self.character, has_effect(effect_2))

    def test_add_multiple_effects_of_same_type(self):
        """
        Adding multiple effects of same type should not be possible
        """
        effect_1 = (EffectBuilder()
                    .with_effect_name('spell')
                    .build())
        effect_2 = (EffectBuilder()
                    .with_effect_name('spell')
                    .build())

        self.character.add_effect(effect_1)
        self.character.add_effect(effect_2)

        assert_that(self.character, has_effect(effect_1))
        assert_that(self.character, is_not(has_effect(effect_2)))

    def test_add_multiple_effects_of_same_type_when_allowed(self):
        """
        In special cases, adding multiple effects of same type is allowed
        """
        effect_1 = (EffectBuilder()
                    .with_effect_name('spell')
                    .with_multiple_allowed()
                    .build())
        effect_2 = (EffectBuilder()
                    .with_effect_name('spell')
                    .with_multiple_allowed()
                    .build())

        self.character.add_effect(effect_1)
        self.character.add_effect(effect_2)

        assert_that(self.character, has_effect(effect_1))
        assert_that(self.character, has_effect(effect_2))


class TestEternalEffects():
    """
    Tests related to effects that do not time out
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.model = None
        self.character1 = None
        self.effect = None
        self.character2 = None

    def setup(self):
        """
        Setup test case
        """
        self.effect = (EffectBuilder()
                       .with_duration(None)
                       .with_frequency(None)
                       .with_tick(None)
                       .build())

        self.model = Model()

        self.character1 = (CharacterBuilder()
                           .as_player_character()
                           .with_model(self.model)
                           .with_tick(10)
                           .build())

        self.character2 = (CharacterBuilder()
                           .with_model(self.model)
                           .with_tick(8)
                           .with_effect(self.effect)
                           .build())

        (LevelBuilder().with_character(self.character1, (2, 2))
                       .with_character(self.character2, (5, 5))
                       .build())

        self.model.player = self.character1

    def test_reducing_tick(self):
        """
        Test that effect with duration, frequency and tick None does
        not cause null reference exception
        """
        self.model.get_next_creature(mock())

    def test_effect_is_not_removed(self):
        """
        Eternal effects should not be removed due to time out
        """
        self.model.get_next_creature(mock())

        assert_that(self.character2, has_effect(self.effect))


class TestEffectsInCombat():
    """
    Test that effects are created correctly during combat
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_effect_is_not_created_on_miss(self):
        """
        Test that effect is not created when attack misses
        """
        to_hit = mock()
        when(to_hit).is_hit().thenReturn(False)

        attacker = CharacterBuilder().build()
        when(attacker).get_effect_handles('on attack hit').thenReturn([mock()])

        factory = mock()
        when(factory).create_effect(any(),
                                    target=any()).thenReturn(mock())

        action = AttackAction(attack_type='',
                              to_hit=to_hit,
                              damage=mock(),
                              attacker=attacker,
                              target=TargetData('character',
                                                (0, 0),
                                                mock(),
                                                None),
                              effect_factory=factory,
                              dying_rules=mock(),
                              additional_rules=mock())

        action.execute()

        verify(factory, never).create_effect(any(),
                                             target=any())

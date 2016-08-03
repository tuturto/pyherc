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
Module for testing effects
"""

from hamcrest import assert_that, equal_to, is_, is_not
from mockito import any, mock, never, verify, when
from pyherc.data import Model
from pyherc.data.effects import Effect, EffectHandle, Heal, Poison
from pyherc.data.geometry import TargetData
from pyherc.generators import get_effect_creator
from pyherc.ports import attack, set_action_factory, drink
from pyherc.rules.combat.action import AttackAction
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  DrinkFactoryBuilder, EffectBuilder,
                                  EffectHandleBuilder, ItemBuilder,
                                  LevelBuilder)
from pyherc.test.matchers import (EventType, has_effect, has_effects,
                                  has_no_effects, event_type_of)


class TestEffects():
    """
    Tests for effects in general
    """

    def test_creating_effect(self):
        """
        Test that effect can be created and triggered immediately
        """
        effect_factory = get_effect_creator({'major heal':
                                  {'type': Heal,
                                   'duration': 0,
                                   'frequency': 0,
                                   'tick': 0,
                                   'healing': 10,
                                   'icon': 101,
                                   'title': 'title',
                                   'description': 'major heal'}})

        potion = (ItemBuilder()
                  .with_effect_handle(EffectHandleBuilder()
                               .with_trigger('on drink')
                               .with_effect('major heal')
                               .with_charges(2))
                  .build())

        set_action_factory(ActionFactoryBuilder()
                           .with_drink_factory(DrinkFactoryBuilder()
                                               .with_effect_factory(effect_factory))  # noqa
                           .build())

        character = (CharacterBuilder()
                     .with_hit_points(1)
                     .with_max_hp(10)
                     .build())

        drink(character,
              potion)

        assert_that(character.hit_points, is_(equal_to(10)))
        assert_that(character, has_no_effects())

    def test_drinking_triggers_effect(self):
        """
        Test that timed effect is triggered only after enough time
        has passed
        """
        effect_factory = get_effect_creator({'major heal':
                                                {'type': Heal,
                                                 'duration': 12,
                                                 'frequency': 3,
                                                 'tick': 3,
                                                 'healing': 10,
                                                 'icon': 100,
                                                 'title': 'healig',
                                                 'description': 'healing'}})

        potion = (ItemBuilder()
                  .with_effect_handle(EffectHandleBuilder()
                               .with_trigger('on drink')
                               .with_effect('major heal')
                               .with_charges(2))
                  .build())

        set_action_factory(ActionFactoryBuilder()
                           .with_drink_factory(DrinkFactoryBuilder()
                                               .with_effect_factory(effect_factory))  # noqa
                           .build())

        character = (CharacterBuilder()
                     .with_hit_points(1)
                     .with_max_hp(10)
                     .build())

        drink(character,
              potion)

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

        verify(model).raise_event(event_type_of('effect removed'))


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

    def setup(self):
        """
        Setup test case
        """
        self.model = mock()

        effects = get_effect_creator({'poison':
                                        {'type': Poison,
                                         'duration': 12,
                                         'frequency': 3,
                                         'tick': 3,
                                         'damage': 5,
                                         'icon': 101,
                                         'title': 'poison',
                                         'description': 'Causes damage'}})

        set_action_factory(ActionFactoryBuilder()
                           .with_attack_factory()
                           .with_effect_factory(effects)
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
               rng)
        attack(self.attacker,
               1,
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
               rng)

        verify(self.model).raise_event(event_type_of('poisoned'))


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

    def test_worn_boots_effects(self):
        """
        Boots' effects are reported as user's effects
        """
        effect = (EffectBuilder()
                  .build())

        item = (ItemBuilder()
                .with_effect(effect)
                .build())

        self.character.inventory.boots = item

        assert_that(self.character, has_effect(effect))


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
                              additional_rules=mock())

        action.execute()

        verify(factory, never).create_effect(any(),
                                             target=any())

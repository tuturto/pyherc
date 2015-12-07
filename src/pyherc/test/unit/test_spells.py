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
Tests for magical spells
"""

from hamcrest import assert_that, equal_to, is_, is_in, greater_than
from mockito import any, mock, verify, when
from pyherc.data.effects import Effect, EffectHandle, Heal
from pyherc.data.magic import Spell
from pyherc.events import e_event_type
from pyherc.generators import create_effect, get_effect_creator
from pyherc.rules.ending import Dying
from pyherc.rules.magic.action import SpellCastingAction
from pyherc.test.builders import (CharacterBuilder, LevelBuilder, SpellBuilder,
                                  SpellGeneratorBuilder)
from pyherc.test.helpers import EventListener


class TestSpellTargetingSingle():
    """
    Tests for spells targeting single character
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
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
                                                  targets = [self.character])

        assert_that(self.character, is_in(spell.targets))

class TestSpellEffects():
    """
    Tests for spell effects
    """

    def __init__(self):
        """
        Default constructor
        """
        self.effect = None
        self.dying_rules = None
        self.effect_handle = None
        self.spell = None
        self.effects = None

    def setup(self):
        """
        Setup test cases
        """
        self.character = (CharacterBuilder()
                          .with_hit_points(10)
                          .with_max_hp(20)
                          .build())

        effect_config = {'healing wind':
                            {'type': Heal,
                             'duration': 0,
                             'frequency': 0,
                             'tick': 0,
                             'healing': 1,
                             'icon': 'icon',
                             'title': 'Cure minor wounds',
                             'description': 'Cures small amount of damage'}}

        self.effects = get_effect_creator(effect_config)

        self.dying_rules = mock(Dying)

        self.effect_handle = EffectHandle(trigger = 'on spell hit',
                                          effect = 'healing wind',
                                          parameters = {},
                                          charges = 1)

        self.spell = (SpellBuilder()
                        .with_effect_handle(self.effect_handle)
                        .with_target(self.character)
                        .build())

    def test_triggering_effect(self):
        """
        Casting a spell should trigger the effect
        """
        self.spell.cast(self.effects,
                        self.dying_rules)

        assert_that(self.character.hit_points, is_(greater_than(10)))

class TestSpellCastingAction():
    """
    Tests for spell casting action
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_spell_is_cast(self):
        """
        When spell casting action is executed, the linked spell should be cast
        """
        spell = mock(Spell)
        spell.spirit = 2

        caster = (CharacterBuilder()
                      .with_spirit(10)
                      .build())

        effects_factory = mock()
        dying_rules = mock()

        action = SpellCastingAction(caster = caster,
                                    spell = spell,
                                    effects_factory = effects_factory,
                                    dying_rules = dying_rules)
        action.execute()

        verify(spell).cast(effects_factory = effects_factory,
                           dying_rules = dying_rules)

    def test_casting_spell_uses_spirit(self):
        """
        Casting a spell should use spirit energy
        """
        spell = (SpellBuilder()
                     .with_spirit(10)
                     .build())

        caster = (CharacterBuilder()
                      .with_spirit(20)
                      .build())
        effects_factory = mock()
        dying_rules = mock()

        action = SpellCastingAction(caster = caster,
                                    spell = spell,
                                    effects_factory = effects_factory,
                                    dying_rules = dying_rules)
        action.execute()

        assert_that(caster.spirit, is_(equal_to(10)))

    def test_casting_spell_raises_spirit_changed_event(self):
        """
        Since casting spells uses spirit, an appropriate event should be raised
        """
        spell = (SpellBuilder()
                     .with_spirit(10)
                     .build())

        caster = (CharacterBuilder()
                      .with_spirit(20)
                      .build())

        listener = EventListener()
        caster.register_for_updates(listener)

        effects_factory = mock()
        dying_rules = mock()

        action = SpellCastingAction(caster = caster,
                                    spell = spell,
                                    effects_factory = effects_factory,
                                    dying_rules = dying_rules)
        action.execute()

        events = [event for event in listener.events
                  if e_event_type(event) == 'spirit points changed']

        assert_that(len(events), is_(equal_to(1)))

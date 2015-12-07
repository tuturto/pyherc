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
Module for magic related tests
"""
#pylint: disable=W0614
from hamcrest import (assert_that,  # pylint: disable-msg=E0611; pylint: disable-msg=E0611
                      contains_inanyorder, equal_to, has_item, is_)
from mockito import any, mock, verify, when
from pyherc.rules import cast
from pyherc.test.builders import (ActionFactoryBuilder, CharacterBuilder,
                                  DamageBuilder, HealBuilder,
                                  SpellCastingFactoryBuilder, SpellEntryBuilder)


class TestMagic:
    """
    Tests for magic
    """

    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_damage_effect(self):
        """
        Test that a damage effect can be applied on a character
        """
        character = (CharacterBuilder()
                        .with_hit_points(15)
                        .with_max_hp(15)
                        .build())

        effect = (DamageBuilder()
                    .with_duration(0)
                    .with_frequency(0)
                    .with_tick(0)
                    .with_damage(10)
                    .with_target(character)
                    .build())

        effect.trigger(mock())

        assert_that(character.hit_points, is_(equal_to(5)))

    def test_healing_effect(self):
        """
        Test that a healing effect can be applied on a character
        """
        character = (CharacterBuilder()
                        .with_hit_points(1)
                        .with_max_hp(15)
                        .build())

        effect = (HealBuilder()
                    .with_duration(0)
                    .with_frequency(0)
                    .with_tick(0)
                    .with_healing(10)
                    .with_target(character)
                    .build())

        effect.trigger(mock())

        assert_that(character.hit_points, is_(equal_to(11)))

    def test_healing_does_not_heal_over_max_hp(self):
        """
        Test that character does not get healed over his maximum hp when getting healing effect
        """
        character = (CharacterBuilder()
                        .with_hit_points(1)
                        .with_max_hp(5)
                        .build())

        effect = (HealBuilder()
                    .with_duration(0)
                    .with_frequency(0)
                    .with_tick(0)
                    .with_healing(10)
                    .with_target(character)
                    .build())

        effect.trigger(mock())

        assert_that(character.hit_points, is_(equal_to(5)))

class TestSpellCasting:
    """
    Test spell casting
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_spell_casting_executes_action(self):
        """
        Casting a spell should activate the action
        """
        magic_factory = SpellCastingFactoryBuilder().build()
        action = mock()
        when(action).is_legal().thenReturn(True)

        when(magic_factory).get_action(any()).thenReturn(action) #pylint: disable-msg=E1103

        action_factory = (ActionFactoryBuilder()
                                    .with_spellcasting_factory(magic_factory)
                                    .build())

        caster = (CharacterBuilder()
                        .build())

        cast(caster,
             direction = 1,
             spell_name = 'healing wind',
             action_factory = action_factory)

        verify(action).execute()

class TestDomains():
    """
    Tests for gaining domains
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_add_domain_level(self):
        """
        Test that a domain level can be added
        """
        caster = (CharacterBuilder()
                        .with_domain('fire', 1)
                        .build())

        caster.add_domain_level('fire')

        assert_that(caster.get_domain_level('fire'), is_(equal_to(2)))

    def test_add_multiple_levels(self):
        """
        Adding more than one level should be possible with a single call
        """
        caster = (CharacterBuilder()
                        .with_domain('fire', 1)
                        .build())

        caster.add_domain_level('fire', 5)

        assert_that(caster.get_domain_level('fire'), is_(equal_to(6)))

    def test_getting_spell_list(self):
        """
        It should be possible to get a list of known spells
        """
        fireball = (SpellEntryBuilder()
                        .with_name('fireball')
                        .with_domain('fire', 1)
                        .build())

        caster = (CharacterBuilder()
                        .with_domain('fire', 1)
                        .with_spell_entry(fireball)
                        .build())

        spells = caster.get_known_spells()

        assert_that(spells, has_item(fireball))

    def test_domains_are_respected(self):
        """
        Domains should not be mixed when listing known spells
        """
        fireball = (SpellEntryBuilder()
                        .with_name('fireball')
                        .with_domain('fire', 1)
                        .build())

        healing_wind = (SpellEntryBuilder()
                            .with_name('healing wind')
                            .with_domain('air', 1)
                            .build())

        caster = (CharacterBuilder()
                        .with_domain('fire', 1)
                        .with_spell_entry(fireball)
                        .with_spell_entry(healing_wind)
                        .build())

        spells = caster.get_known_spells()

        assert_that(spells, contains_inanyorder(fireball, ))

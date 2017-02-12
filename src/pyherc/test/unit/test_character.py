# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
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
Module for testing characters
"""
from hamcrest import assert_that, equal_to, is_
from mockito import mock, verify
from pyherc.data import WeaponProficiency
from pyherc.events import new_move_event
from pyherc.test.builders import CharacterBuilder, ItemBuilder
from pyherc.test.matchers import EventType


class TestCharacter():
    """
    Tests for character
    """
    def __init__(self):
        super().__init__()

    def test_event_is_raised_for_hp_change(self):
        """
        Event should be raised when hit points change
        """
        listener = mock()

        character = (CharacterBuilder()
                     .with_update_listener(listener)
                     .build())

        character.hit_points = 20

        verify(listener).receive_update(EventType('hit points changed'))

    def test_raising_event(self):
        """
        Test that character can raise event
        """
        model = mock()
        character = (CharacterBuilder()
                     .with_model(model)
                     .build())

        character.raise_event(new_move_event(character=character,
                                             old_location=character.location,
                                             old_level=None,
                                             direction=1))

        verify(model).raise_event(EventType('move'))


class TestCreatures():
    """
    Tests for creatures that require generators to be working
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_is_proficient(self):
        """
        Test that weapon proficiency of character can be checked
        """
        creature = CharacterBuilder().build()

        weapon = (ItemBuilder()
                  .with_name('club')
                  .with_tag('weapon')
                  .with_tag('one-handed weapon')
                  .with_tag('melee')
                  .with_tag('simple weapon')
                  .with_damage(2, 'bashing')
                  .with_weapon_type('simple')
                  .build())

        proficiency = creature.is_proficient(weapon)
        assert_that(proficiency, is_(equal_to(False)))

        creature.feats.append(WeaponProficiency('simple'))

        proficiency = creature.is_proficient(weapon)
        assert_that(proficiency, is_(equal_to(True)))

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
Module for testing poison related rules
"""
#pylint: disable=W0614
from hamcrest import assert_that, equal_to, is_  # pylint: disable-msg=E0611
from mockito import mock, verify
from pyherc.data.effects import Poison
from pyherc.generators import get_effect_creator
from pyherc.test.builders import CharacterBuilder, PoisonBuilder
from pyherc.test.matchers import EventType, has_effect


class TestPoison():
    """
    Basic tests for poison
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_event_is_raised_on_trigger(self):
        """
        Test that event is raised when poison is triggered
        """
        model = mock()

        character = (CharacterBuilder()
                        .with_hit_points(10)
                        .with_model(model)
                        .build())

        poison = (PoisonBuilder()
                    .with_target(character)
                    .build())

        poison.trigger()

        verify(model).raise_event(EventType('poison triggered'))

class TestEffectsFactory():
    """
    Poison related tests for effects factory
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_creating_poison(self):
        """
        Test that poison effect can be created
        """
        character = CharacterBuilder().build()
        effects = get_effect_creator({'poison':
                                        {'type': Poison,
                                         'duration': 150,
                                         'frequency': 30,
                                         'tick': 10,
                                         'damage': 5,
                                         'icon': 101,
                                         'title': 'Moderate poison',
                                         'description': 'Causes damage'}})

        effect = effects('poison', target = character)

        assert_that(effect.duration, is_(equal_to(150)))
        assert_that(effect.frequency, is_(equal_to(30)))
        assert_that(effect.damage, is_(equal_to(5)))
        assert_that(effect.target, is_(equal_to(character)))
        assert_that(effect.icon, is_(equal_to(101)))
        assert_that(effect.title, is_(equal_to('Moderate poison')))
        assert_that(effect.description, is_(equal_to('Causes damage')))

    def test_creating_poison_with_paramarray(self):
        """
        Test that poison can be created by passing it a parameter array
        """
        character = CharacterBuilder().build()

        params = {'duration': 150,
                  'frequency': 30,
                  'tick': 10,
                  'damage': 1,
                  'target': character,
                  'icon': 101,
                  'title': 'Moderate poison',
                  'description': 'Causes damage'}

        effect = Poison(**params)

        assert_that(effect.duration, is_(equal_to(150)))
        assert_that(effect.frequency, is_(equal_to(30)))
        assert_that(effect.damage, is_(equal_to(1)))
        assert_that(effect.target, is_(equal_to(character)))
        assert_that(effect.icon, is_(equal_to(101)))
        assert_that(effect.title, is_(equal_to('Moderate poison')))
        assert_that(effect.description, is_(equal_to('Causes damage')))

class TestCharacter():
    """
    Test Character methods related to poison
    """
    def __init__(self):
        """
        Default constructor
        """

    def test_adding_effect(self):
        """
        Test that poison effect can be added to a character
        """
        character = CharacterBuilder().build()
        poison = mock(Poison)

        character.add_effect(poison)

        assert_that(character, has_effect(poison))

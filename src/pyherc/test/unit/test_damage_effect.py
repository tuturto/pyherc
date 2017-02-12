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
Tests for damage effect
"""
from mockito import any, mock, verify, when
from hamcrest import assert_that, is_, equal_to
from pyherc.data import Character
from pyherc.data.effects import DamageModifier
from pyherc.test.builders import CharacterBuilder, DamageBuilder
from pyherc.test.matchers import event_type_of


class TestDamageEffect():
    """
    Tests for damage effect
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_triggering_damage_raises_event(self):
        """
        Triggering damage effect should raise a proper event
        """
        model = mock()
        target = (CharacterBuilder()
                  .with_model(model)
                  .build())

        effect = (DamageBuilder()
                  .with_target(target)
                  .build())

        effect.trigger()

        verify(model).raise_event(event_type_of('damage triggered'))

    def test_triggering_damage_respects_damage_modifier(self):
        """
        Damage modifier should be respected
        """
        model = mock()

        target = (CharacterBuilder()
                  .with_model(model)
                  .with_hit_points(10)
                  .with_effect(DamageModifier(modifier=-5,
                                              damage_type='magical',
                                              duration=0,
                                              frequency=0,
                                              tick=0,
                                              icon=0,
                                              title='resistance',
                                              description='resistance'))
                  .build())

        effect = (DamageBuilder()
                  .with_target(target)
                  .with_damage(5)
                  .build())

        effect.trigger()

        assert_that(target.hit_points, is_(equal_to(10)))

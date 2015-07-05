# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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

        effect.trigger(dying_rules=mock())

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

        effect.trigger(dying_rules=mock())

        assert_that(target.hit_points, is_(equal_to(10)))

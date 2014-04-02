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
Tests for damage effect
"""
from mockito import any, mock, verify
from pyherc.test.builders import DamageBuilder


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
        target = mock()
        target.hit_points = 10
        effect = (DamageBuilder()
                  .with_target(target)
                  .build())

        effect.trigger(dying_rules=mock())

        verify(target).raise_event(any())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Tests for damage
"""

from pyherc.rules.attack.action import Damage
from hamcrest import assert_that, is_, equal_to, only_contains

class TestDamage(object):
    """
    Tests for damage
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestDamage, self).__init__()

        self.damage = None

    def setup(self):
        """
        Setup test cases
        """
        self.damage = Damage([(2, 'crushing'),
                              (4, 'fire')])

    def test_total_damage_is_calculated(self):
        """
        Total amount of damage should be sum of its parts
        """
        assert_that(self.damage.damage, is_(equal_to(6)))

    def test_damage_type(self):
        """
        Type of damage should be reported
        """
        assert_that(self.damage.damage_types, only_contains('crushing',
                                                            'fire'))

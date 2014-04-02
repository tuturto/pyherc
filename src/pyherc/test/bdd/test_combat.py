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
Package for combat tests
"""
from hamcrest import assert_that
from pyherc.test.cutesy import Adventurer, Dagger, Goblin, strong, weak
from pyherc.test.cutesy.dictionary import (has_less_hit_points, hit, Level,
                                           make, middle_of, place, right_of,
                                           wielding)


class TestCombatBehaviour():
    """
    Combat related behaviour
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_hitting_reduces_hit_points(self):
        """
        Getting hit should reduce hit points
        """
        Pete = strong(Adventurer())
        Uglak = weak(Goblin())

        place(Uglak, middle_of(Level()))
        place(Pete, right_of(Uglak))

        make(Uglak, hit(Pete))

        assert_that(Pete, has_less_hit_points())

    def test_hitting_with_weapon_reduces_hit_points(self):
        """
        Getting hit by weapon should reduce hit points
        """
        Pete = strong(Adventurer())
        Uglak = weak(Goblin(wielding(Dagger())))

        place(Uglak, middle_of(Level()))
        place(Pete, right_of(Uglak))

        make(Uglak, hit(Pete))

        assert_that(Pete, has_less_hit_points())

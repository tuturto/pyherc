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

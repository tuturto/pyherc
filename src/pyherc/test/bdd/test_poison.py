#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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

from pyherc.test.cutesy.dictionary import weak, Goblin
from pyherc.test.cutesy.dictionary import strong, Adventurer
from pyherc.test.cutesy.dictionary import Level
from pyherc.test.cutesy.dictionary import place, middle_of
from pyherc.test.cutesy import affect, with_, potent_poison, weak_poison
from pyherc.test.cutesy.dictionary import has_less_hit_points
from pyherc.test.matchers import is_dead, is_not_at
from hamcrest import assert_that

class TestPoison(object):
    """
    Tests for poison
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestPoison, self).__init__()

    def test_poison_causes_damage(self):
        """
        Test that triggered poison will damage character
        """
        Pete = strong(Adventurer())

        affect(Pete, with_(weak_poison()))

        assert_that(Pete, has_less_hit_points())

    def test_character_can_die_from_poisoning(self):
        """
        Test that character with less than 1 hit points is removed from play
        """
        Uglak = weak(Goblin())
        room = Level()
        place(Uglak, middle_of(room))

        affect(Uglak, with_(potent_poison()))

        assert_that(Uglak, is_dead())
        assert_that(Uglak, is_not_at(room))

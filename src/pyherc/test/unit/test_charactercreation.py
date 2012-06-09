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
#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

"""
Module for testing character creation
"""
#pylint: disable=W0614
import pyherc.rules.character
from hamcrest import * #pylint: disable=W0401

class TestCharacterCreation(object):
    """
    Tests for character creation
    """
    def test_creation(self):
        """
        Test that simple character creation works
        """
        pyherc.rules.character.initialise_stat_tables()
        character = pyherc.rules.character.create_character(
                                        race = 'human',
                                        kit = 'fighter',
                                        model = None,
                                        action_factory = None,
                                        rng = None)

        assert_that(character, is_(not_none()))

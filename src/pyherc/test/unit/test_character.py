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
Module for testing characters
"""
#pylint: disable=W0614
from pyherc.data import Model
from pyherc.data import WeaponProficiency
from pyherc.test.builders import CharacterBuilder
from pyherc.test.builders import ItemBuilder
from pyherc.test.builders import LevelBuilder
from pyherc.data.dungeon import Dungeon
from pyherc.test.matchers import EventType
from hamcrest import assert_that, is_, same_instance, equal_to, none #pylint: disable-msg=E0611
from pyherc.events import MoveEvent
from mockito import mock, verify

class TestCharacter():
    """
    Tests for character
    """
    def __init__(self):
        super(TestCharacter, self).__init__()

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

        level = (LevelBuilder()
                    .with_character(character)
                    .build())

        character.raise_event(MoveEvent(mover = character,
                                        affected_tiles = []))

        verify(model).raise_event(EventType('move'))

class TestCreatures():
    """
    Tests for creatures that require generators to be working
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestCreatures, self).__init__()

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

class TestStatues():
    """
    Test handling of statues (mainly mimicing items)
    """

    def __init__(self):
        """
        Default constructor
        """
        super(TestStatues, self).__init__()

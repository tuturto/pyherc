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
Module for testing ranged combat related rules
"""
from pyherc.rules.combat import RangedCombatFactory
from pyherc.rules.combat.interface import AttackParameters
from pyherc.rules import attack
from pyherc.test.matchers import AttackActionParameterMatcher, does_have
from pyherc.test.builders import LevelBuilder, CharacterBuilder, ItemBuilder
from pyherc.test.builders import ActionFactoryBuilder
from mockito import verify, mock, when, any
from hamcrest import assert_that, is_, equal_to, is_not #pylint: disable-msg=E0611
from random import Random

class TestRangedCombat():
    """
    Tests for ranged combat
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.level = None
        self.character = None
        self.target = None
        self.action_factory = None

    def setup(self):
        """
        Setup test cases
        """
        self.character = (CharacterBuilder()
                            .with_location((2, 2))
                            .with_hit_points(10)
                            .build())

        self.target = (CharacterBuilder()
                            .with_location((5, 2))
                            .with_hit_points(10)
                            .build())

        self.level = (LevelBuilder()
                        .with_character(self.character)
                        .with_character(self.target)
                        .build())

        bow = (ItemBuilder()
                    .with_name('bow')
                    .with_required_ammunition_type('arrow')
                    .with_damage(1, 'crushing')
                    .build())
        self.arrows = (ItemBuilder()
                        .with_name('arrows')
                        .with_ammunition_type('arrow')
                        .with_range_damage(3, 'piercing')
                        .with_count(10)
                        .build())

        self.character.inventory.append(bow)
        self.character.inventory.append(self.arrows)
        self.character.inventory.weapon = bow
        self.character.inventory.projectiles = self.arrows

        self.action_factory = mock()
        when(self.action_factory).get_action(any()).thenReturn(mock())

    def test_ranged_attack_is_created_for_distant_enemy(self):
        """
        When attacking enemy in distance, a ranged attack should
        be created
        """
        attack(self.character,
               3,
               self.action_factory,
               Random())

        verify(self.action_factory).get_action(
                            AttackActionParameterMatcher(
                                        attack_type = 'ranged'))

    def test_damage_for_ranged_attack_is_from_arrow(self):
        """
        Damage for ranged attack comes from the arrow
        """
        action_factory = (ActionFactoryBuilder()
                            .with_attack_factory()
                            .build())

        attack(self.character,
               3,
               action_factory,
               Random())

        assert_that(self.target.hit_points, is_(equal_to(7)))

    def test_ammunition_is_decreased(self):
        """
        Ranged attack should use ammunition
        """
        action_factory = (ActionFactoryBuilder()
                            .with_attack_factory()
                            .build())

        attack(self.character,
               3,
               action_factory,
               Random())

        assert_that(self.arrows.ammunition_data.count, is_(equal_to(9)))

    def test_depleted_ammunition_is_removed(self):
        """
        Completely spent ammunition should be removed from inventory
        """
        action_factory = (ActionFactoryBuilder()
                            .with_attack_factory()
                            .build())

        self.arrows.ammunition_data.count = 1

        attack(self.character,
               3,
               action_factory,
               Random())

        assert_that(self.character, is_not(does_have(self.arrows)))

    def test_melee_attack_is_created_for_close_enemy(self):
        """
        Even when character is armed with ranged weapon, he can not use
        ranged attack against enemy that is standing right next to him
        """
        self.target.location = (self.character.location[0] + 1,
                                self.character.location[1])

        attack(self.character,
               3,
               self.action_factory,
               Random())

        verify(self.action_factory).get_action(
                            AttackActionParameterMatcher(
                                        attack_type = 'melee'))

    def test_finding_target(self):
        """
        Test that factory can find the target
        """
        factory = RangedCombatFactory(effect_factory = mock(),
                                      dying_rules = mock())

        target = factory.get_target(
                            AttackParameters(
                                        attacker = self.character,
                                        direction = 3,
                                        attack_type = 'ranged',
                                        random_number_generator = Random()))

        assert_that(target.target, is_(equal_to(self.target)))

    def test_target_is_not_located_behind_wall(self):
        """
        Walls should block arrows
        """
        factory = RangedCombatFactory(effect_factory = mock(),
                                      dying_rules = mock())

        x_loc = self.character.location[0] + 1
        y_loc = self.character.location[1]

        self.level.walls[x_loc][y_loc] = 100

        target = factory.get_target(
                            AttackParameters(
                                        attacker = self.character,
                                        direction = 3,
                                        attack_type = 'ranged',
                                        random_number_generator = Random()))

        assert_that(target, is_not(equal_to(self.target)))

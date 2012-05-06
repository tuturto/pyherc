#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
Module for character builder
"""
from pyherc.data import Character
from mockito import mock
from random import Random

class CharacterBuilder(object):
    """
    Class for building Characters
    """
    def __init__(self):
        """
        Default constructor
        """
        super(CharacterBuilder, self).__init__()
        self.hit_points = 10
        self.max_hp = 10
        self.model = mock()
        self.action_factory = mock()
        self.rng = Random()

        self.speed = 1
        self.tick = 0
        self.attack = 1
        self.body = 1

        self.level = None
        self.location = ()

    def with_model(self, model):
        self.model = model
        return self

    def with_action_factory(self, factory):
        self.action_factory = factory
        return self

    def with_rng(self, rng):
        self.rng = rng
        return self

    def with_hit_points(self, hit_points):
        self.hit_points = hit_points
        return self

    def with_max_hp(self, max_hp):
        self.max_hp = max_hp
        return self

    def with_speed(self, speed):
        self.speed = speed
        return self

    def with_tick(self, tick):
        self.tick = tick
        return self

    def with_attack(self, attack):
        self.attack = attack
        return self

    def with_body(self, body):
        self.body = body
        return self

    def with_level(self, level):
        self.level = level
        return self

    def with_location(self, location):
        self.location = location
        return self

    def build(self):
        """
        Build character

        Returns:
            Character
        """
        character = Character(model = self.model,
                              action_factory = self.action_factory,
                              rng = self.rng)

        character.hit_points = self.hit_points
        character.max_hp = self.max_hp

        character.body = self.body
        character.attack = self.attack

        character.speed = self.speed
        character.tick = self.tick
        character.level = self.level
        character.location = self.location

        return character

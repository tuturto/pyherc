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
Module for action factory builders
"""
from mockito import mock

from pyherc.rules.public import ActionFactory
from pyherc.rules.move.factories import MoveFactory, WalkFactory
from pyherc.rules.attack.factories import AttackFactory
from pyherc.rules.attack.factories import UnarmedCombatFactory
from pyherc.rules.attack.factories import MeleeCombatFactory
from pyherc.rules.consume.factories import DrinkFactory
from pyherc.rules.inventory.factories import InventoryFactory
from pyherc.rules.inventory.factories import PickUpFactory

class ActionFactoryBuilder(object):
    """
    Class for building action factories
    """
    def __init__(self):
        self.model = mock()

        self.attack_factory = mock()
        self.attack_factory.action_type = 'attack'
        self.drink_factory = mock()
        self.drink_factory.action_type = 'drink'
        self.inventory_factory = mock()
        self.inventory_factory.action_type = 'inventory'
        self.move_factory = mock()
        self.move_factory.action_type = 'move'

        self.effect_factory = mock()
        self.use_real_attack_factory = False
        self.use_real_drink_factory = False
        self.use_real_inventory_factory = False
        self.use_real_move_factory = False

    def with_model(self, model):
        self.model = model
        return self

    def with_move_factory(self):
        self.use_real_move_factory = True
        return self

    def with_attack_factory(self):
        self.use_real_attack_factory = True
        return self

    def with_drink_factory(self):
        self.use_real_drink_factory = True
        return self

    def with_inventory_factory(self):
        self.use_real_inventory_factory = True
        return self

    def with_effect_factory(self, effect_factory):
        self.effect_factory = effect_factory
        return self

    def build(self):
        if self.use_real_attack_factory == True:
            unarmed_combat_factory = UnarmedCombatFactory(self.effect_factory)
            melee_combat_factory = MeleeCombatFactory(self.effect_factory)
            self.attack_factory = AttackFactory([
                                        unarmed_combat_factory,
                                        melee_combat_factory])

        if self.use_real_drink_factory == True:
            drink_factory = DrinkFactory(self.effect_factory)

        if self.use_real_inventory_factory == True:
            pick_up_factory = PickUpFactory()
            self.inventory_factory = InventoryFactory([
                                            pick_up_factory])

        if self.use_real_move_factory == True:
            walk_factory = WalkFactory()
            self.move_factory = MoveFactory(walk_factory)

        action_factory = ActionFactory(self.model,
                                       [self.move_factory,
                                        self.drink_factory,
                                        self.attack_factory,
                                        self.inventory_factory])

        return action_factory

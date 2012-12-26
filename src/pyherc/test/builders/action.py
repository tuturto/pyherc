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

"""
Module for action factory builders
"""
from mockito import mock

from pyherc.rules.public import ActionFactory
from pyherc.rules import Dying
from pyherc.rules.move.factories import MoveFactory, WalkFactory
from pyherc.rules.attack.factories import AttackFactory
from pyherc.rules.attack.factories import UnarmedCombatFactory
from pyherc.rules.attack.factories import MeleeCombatFactory
from pyherc.rules.attack import RangedCombatFactory
from pyherc.rules.consume.factories import DrinkFactory
from pyherc.rules.inventory.factories import InventoryFactory
from pyherc.rules.inventory.factories import PickUpFactory, DropFactory
from pyherc.rules.inventory.equip import EquipFactory
from pyherc.rules.inventory.unequip import UnEquipFactory

class ActionFactoryBuilder(object):
    """
    Class for building action factories
    """
    def __init__(self):
        """
        Default constructor
        """
        self.model = mock()

        self.attack_factory = mock()
        self.attack_factory.action_type = 'attack'
        self.drink_factory = mock()
        self.drink_factory.action_type = 'drink'
        self.inventory_factory = mock()
        self.inventory_factory.action_type = 'inventory'
        self.move_factory = mock()
        self.move_factory.action_type = 'move'
        self.dying_rules = mock()

        self.effect_factory = mock()
        self.use_real_attack_factory = False
        self.use_real_drink_factory = False
        self.use_real_inventory_factory = False
        self.use_real_move_factory = False
        self.use_real_dying_rules = False

    def with_model(self, model):
        """
        Set model to use with factory

        :param model: model
        :type model: Model
        """
        self.model = model
        return self

    def with_move_factory(self):
        """
        Configure action factory to use real move factory
        """
        self.use_real_move_factory = True
        return self

    def with_attack_factory(self):
        """
        Configure action factory to use real attack factory
        """
        self.use_real_attack_factory = True
        return self

    def with_drink_factory(self, drink_factory = None):
        """
        Configure action factory to use real drink factory
        """
        if drink_factory == None:
            self.use_real_drink_factory = True
        else:
            if hasattr(drink_factory, 'build'):
                self.drink_factory = drink_factory.build()
            else:
                self.drink_factory = drink_factory
        return self

    def with_inventory_factory(self):
        """
        Configure action factory to use real inventory factory
        """
        self.use_real_inventory_factory = True
        return self

    def with_effect_factory(self, effect_factory):
        """
        Configure action factory to use effect factory

        :param effect_factory: effect factory to use
        :type effect_factory: EffectFactory
        """
        self.effect_factory = effect_factory
        return self

    def with_dying_rules(self):
        """
        Configure action factory to use dying rules
        """
        self.use_real_dying_rules = True
        return self

    def build(self):
        """
        Build action factory

        :returns: action factory
        :rtype: ActionFactory
        """
        if self.use_real_dying_rules == True:
            self.dying_rules = Dying()

        if self.use_real_attack_factory == True:
            unarmed_combat_factory = UnarmedCombatFactory(self.effect_factory,
                                                          self.dying_rules)
            melee_combat_factory = MeleeCombatFactory(self.effect_factory,
                                                      self.dying_rules)
            ranged_combat_factory = RangedCombatFactory(self.effect_factory,
                                                        self.dying_rules)
            self.attack_factory = AttackFactory([
                                        unarmed_combat_factory,
                                        melee_combat_factory,
                                        ranged_combat_factory])

        if self.use_real_drink_factory == True:
            self.drink_factory = (DrinkFactoryBuilder()
                                    .with_effect_factory(self.effect_factory)
                                    .with_dying_rules(self.dying_rules)
                                    .build())

        if self.use_real_inventory_factory == True:
            pick_up_factory = PickUpFactory()
            drop_factory = DropFactory()
            equip_factory = EquipFactory()
            unequip_factory = UnEquipFactory()
            self.inventory_factory = InventoryFactory([
                                            pick_up_factory,
                                            drop_factory,
                                            equip_factory,
                                            unequip_factory])

        if self.use_real_move_factory == True:
            walk_factory = WalkFactory(mock())
            self.move_factory = MoveFactory(walk_factory)

        action_factory = ActionFactory(self.model,
                                       [self.move_factory,
                                        self.drink_factory,
                                        self.attack_factory,
                                        self.inventory_factory])

        return action_factory

class DrinkFactoryBuilder(object):
    """
    Class to build drink factories
    """
    def __init__(self):
        """
        Default constructor
        """
        super(DrinkFactoryBuilder, self).__init__()

        self.effect_factory = mock()
        self.dying_rules = mock()

        self.use_real_dying_rules = False

    def with_effect_factory(self, effect_factory):
        """
        Set effect factory to use
        """
        self.effect_factory = effect_factory
        return self

    def with_dying_rules(self, dying_rules = None):
        """
        Set dying rules to use
        """
        if dying_rules != None:
            self.dying_rules = dying_rules
        else:
            self.use_real_dying_rules = True
        return self

    def build(self):
        """
        Builds drink factory
        """
        if self.use_real_dying_rules == True:
            self.dying_rules = Dying()

        return DrinkFactory(self.effect_factory,
                            self.dying_rules)

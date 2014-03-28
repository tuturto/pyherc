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
Module for action factory builders
"""
from mockito import mock

from pyherc.rules.public import ActionFactory
from pyherc.rules import Dying
from pyherc.rules.moving.factories import MoveFactory, WalkFactory
from pyherc.rules.combat.factories import AttackFactory
from pyherc.rules.combat.factories import UnarmedCombatFactory
from pyherc.rules.combat.factories import MeleeCombatFactory
from pyherc.rules.combat import RangedCombatFactory
from pyherc.rules.consume.factories import DrinkFactory
from pyherc.rules.inventory.factories import InventoryFactory
from pyherc.rules.inventory.factories import PickUpFactory, DropFactory
from pyherc.rules.inventory.equip import EquipFactory
from pyherc.rules.inventory.unequip import UnEquipFactory
from pyherc.rules.magic import SpellCastingFactory, GainDomainFactory
from pyherc.rules.waiting.factories import WaitFactory


class ActionFactoryBuilder():
    """
    Class for building action factories
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.model = mock()

        self.attack_factory = mock()
        self.attack_factory.action_type = 'attack'
        self.drink_factory = mock()
        self.drink_factory.action_type = 'drink'
        self.inventory_factory = mock()
        self.inventory_factory.action_type = 'inventory'
        self.move_factory = mock()
        self.move_factory.action_type = 'move'
        self.spellcasting_factory = mock()
        self.spellcasting_factory.action_type = 'cast spell'
        self.wait_factory = mock()
        self.wait_factory.action_type = 'wait'
        self.gain_domain_factory = mock()
        self.gain_domain_factory.action_type = 'gain domain'
        self.dying_rules = mock()

        self.effect_factory = mock()
        self.use_real_attack_factory = False
        self.use_real_drink_factory = False
        self.use_real_inventory_factory = False
        self.use_real_move_factory = False
        self.use_real_spellcasting_factory = False
        self.use_real_wait_factory = False
        self.use_real_gain_domain_factory = False
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

    def with_drink_factory(self, drink_factory=None):
        """
        Configure action factory to use real drink factory
        """
        if drink_factory is None:
            self.use_real_drink_factory = True
        else:
            if hasattr(drink_factory, 'build'):
                self.drink_factory = drink_factory.build()
            else:
                self.drink_factory = drink_factory
        return self

    def with_spellcasting_factory(self, spellcasting_factory=None):
        """
        Configure action factory to use real magic factory

        .. versionadded:: 0.9
        """
        if not spellcasting_factory:
            self.use_real_spellcasting_factory = True
        else:
            if hasattr(spellcasting_factory, 'build'):
                self.spellcasting_factory = spellcasting_factory.build()
            else:
                self.spellcasting_factory = spellcasting_factory
        return self

    def with_wait_factory(self, wait_factory=None):
        """
        Configure wait factory to use

        .. versionadded:: 0.10
        """
        if not wait_factory:
            self.use_real_wait_factory = True
        else:
            if hasattr(wait_factory, 'build'):
                self.wait_factory = wait_factory.build()
            else:
                self.wait_factory = wait_factory
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

    def with_gain_domain_factory(self, gain_domain_factory=None):
        """
        Configure action factory to use gain domain factory

        :param gain_domain_factory: gain domain factory to use
        :type gain_domain_factory: GainDomainFactory

        .. versionadded:: 0.10
        """
        if gain_domain_factory:
            self.gain_domain_factory = gain_domain_factory
        else:
            self.use_real_gain_domain_factory = True

        return self

    def build(self):
        """
        Build action factory

        :returns: action factory
        :rtype: ActionFactory
        """
        if self.use_real_dying_rules:
            self.dying_rules = Dying()

        if self.use_real_attack_factory:
            unarmed_combat_factory = UnarmedCombatFactory(self.effect_factory,
                                                          self.dying_rules)
            melee_combat_factory = MeleeCombatFactory(self.effect_factory,
                                                      self.dying_rules)
            ranged_combat_factory = RangedCombatFactory(self.effect_factory,
                                                        self.dying_rules)
            self.attack_factory = AttackFactory([unarmed_combat_factory,
                                                 melee_combat_factory,
                                                 ranged_combat_factory])

        if self.use_real_drink_factory:
            self.drink_factory = (DrinkFactoryBuilder()
                                  .with_effect_factory(self.effect_factory)
                                  .with_dying_rules(self.dying_rules)
                                  .build())

        if self.use_real_inventory_factory:
            pick_up_factory = PickUpFactory()
            drop_factory = DropFactory()
            equip_factory = EquipFactory()
            unequip_factory = UnEquipFactory()
            self.inventory_factory = InventoryFactory([pick_up_factory,
                                                       drop_factory,
                                                       equip_factory,
                                                       unequip_factory])

        if self.use_real_move_factory:
            walk_factory = WalkFactory(mock(), mock())
            self.move_factory = MoveFactory(walk_factory)

        if self.use_real_spellcasting_factory:
            self.spellcasting_factory = SpellCastingFactoryBuilder().build()

        if self.use_real_wait_factory:
            self.wait_factory = WaitFactoryBuilder().build()

        if self.use_real_gain_domain_factory:
            self.gain_domain_factory = GainDomainFactoryBuilder().build()

        action_factory = ActionFactory(self.model,
                                       [self.move_factory,
                                        self.drink_factory,
                                        self.attack_factory,
                                        self.inventory_factory,
                                        self.spellcasting_factory,
                                        self.wait_factory,
                                        self.gain_domain_factory])

        return action_factory


class DrinkFactoryBuilder():
    """
    Class to build drink factories
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.effect_factory = mock()
        self.dying_rules = mock()

        self.use_real_dying_rules = False

    def with_effect_factory(self, effect_factory):
        """
        Set effect factory to use
        """
        self.effect_factory = effect_factory
        return self

    def with_dying_rules(self, dying_rules=None):
        """
        Set dying rules to use
        """
        if dying_rules is not None:
            self.dying_rules = dying_rules
        else:
            self.use_real_dying_rules = True
        return self

    def build(self):
        """
        Builds drink factory
        """
        if self.use_real_dying_rules:
            self.dying_rules = Dying()

        return DrinkFactory(self.effect_factory,
                            self.dying_rules)


class WaitFactoryBuilder():
    """
    Builder for wait factory

    .. versionadded:: 0.10
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def build(self):
        """
        Build wait factory
        """
        return WaitFactory()


class GainDomainFactoryBuilder():
    """
    Builder for gain domain factory

    ..versionadded:: 0.10
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def build(self):
        """
        Builds the factory
        """
        return GainDomainFactory()


class SpellCastingFactoryBuilder():
    """
    Builder for spell casting factory

    .. versionadded:: 0.9
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.spell_factory = mock()
        self.use_real_spell_factory = False
        self.effects_factory = mock()
        self.use_real_effects_factory = False

    def with_spell_factory(self, spell_factory=None):
        """
        Configure spell factory to use
        """
        if not spell_factory:
            self.use_real_spell_factory = True
        else:
            if hasattr(spell_factory, 'build'):
                self.spell_factory = spell_factory.build()
            else:
                self.spell_factory = spell_factory
        return self

    def with_effects_factory(self, effects_factory=None):
        """
        Configure effects factory to use
        """
        if effects_factory:
            if hasattr(effects_factory, 'build'):
                self.effects_factory = effects_factory.build()
            else:
                self.effects_factory = effects_factory
        else:
            self.use_real_effects_factory = True
        return self

    def build(self):
        """
        Builds spell casting factory
        """
        if self.use_real_spell_factory:
            #self.spell_factory = None
            pass

        if self.use_real_effects_factory:
            #self.effects_factory = None
            pass

        return SpellCastingFactory(spell_factory=self.spell_factory,
                                   effects_factory=self.effects_factory,
                                   dying_rules=Dying())

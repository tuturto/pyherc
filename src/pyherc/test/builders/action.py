# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
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
Module for action factory builders
"""
from pyherc.rules import Dying
from pyherc.rules.combat import RangedCombatFactory
from pyherc.rules.combat.factories import (AttackFactory, MeleeCombatFactory,
                                           UnarmedCombatFactory)
from pyherc.rules.consume.factories import DrinkFactory
from pyherc.rules.digging.factories import DigFactory
from pyherc.rules.inventory.equip import EquipFactory
from pyherc.rules.inventory.factories import (DropFactory, InventoryFactory,
                                              PickUpFactory)
from pyherc.rules.inventory.unequip import UnEquipFactory
from pyherc.rules.magic import GainDomainFactory, SpellCastingFactory
from pyherc.rules.mitosis.factory import MitosisFactory
from pyherc.rules.metamorphosis.factory import MetamorphosisFactory
from pyherc.rules.moving.factories import MoveFactory
from pyherc.rules.trapping.factory import TrappingFactory
from pyherc.rules.public import ActionFactory
from pyherc.rules.waiting.factories import WaitFactory
from random import Random


class ActionFactoryBuilder():
    """
    Class for building action factories
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.model = None

        self.factories = []

        self.dying_rules = Dying()
        self.effect_factory = None
        self.use_real_attack_factory = False
        self.use_real_drink_factory = False
        self.use_real_inventory_factory = False
        self.use_real_move_factory = False
        self.use_real_spellcasting_factory = False
        self.use_real_wait_factory = False
        self.use_real_gain_domain_factory = False
        self.use_real_dying_rules = False
        self.use_real_mitosis_factory = False
        self.use_real_metamorphosis_factory = False
        self.use_real_dig_factory = False
        self.use_real_trapping_factory = False

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
                
                self.factories.append(drink_factory.build())
            else:
                self.factories.append(drink_factory)
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
                self.factories.append(spellcasting_factory.build())
            else:
                self.factories.append(spellcasting_factory)
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
                self.factories.append(wait_factory.build())
            else:
                self.factories.append(wait_factory)
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
            self.factories.append(gain_domain_factory)
        else:
            self.use_real_gain_domain_factory = True

        return self

    def with_mitosis_factory(self, mitosis_factory=None):
        """
        Configure action factory to use mitosis factory
        """
        if mitosis_factory:
            self.factories.append(mitosis_factory)
        else:
            self.use_real_mitosis_factory = True

        return self

    def with_metamorphosis_factory(self, metamorphosis_factory=None):
        """
        Configure metamorphosis factory to use
        """
        if metamorphosis_factory:
            self.factories.append(metamorphosis_factory)
        else:
            self.use_real_metamorphosis_factory = True

        return self

    def with_dig_factory(self, dig_factory=None):
        if dig_factory:
            self.factories.append(dig_factory)
        else:
            self.use_real_dig_factory = True

        return self

    def with_trapping_factory(self, trapping_factory=None):
        if trapping_factory:
            self.factories.append(trapping_factory)
        else:
            self.use_real_trapping_factory = True

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
            self.factories.append(AttackFactory([unarmed_combat_factory,
                                                 melee_combat_factory,
                                                 ranged_combat_factory]))

        if self.use_real_drink_factory:
            self.factories.append((DrinkFactoryBuilder()
                                   .with_effect_factory(self.effect_factory)
                                   .with_dying_rules(self.dying_rules)
                                   .build()))

        if self.use_real_inventory_factory:
            self.factories.append(InventoryFactory([PickUpFactory(),
                                                    DropFactory(),
                                                    EquipFactory(),
                                                    UnEquipFactory()]))

        if self.use_real_move_factory:
            self.factories.append(MoveFactory(None, self.dying_rules))

        if self.use_real_spellcasting_factory:
            self.factories.append(SpellCastingFactoryBuilder().build())

        if self.use_real_wait_factory:
            self.factories.append(WaitFactoryBuilder().build())

        if self.use_real_gain_domain_factory:
            self.factories.append(GainDomainFactoryBuilder().build())

        if self.use_real_mitosis_factory:
            self.factories.append(MitosisFactoryBuilder()
                                  .with_dying_rules(self.dying_rules)
                                  .build())

        if self.use_real_metamorphosis_factory:
            self.factories.append(MetamorphosisFactoryBuilder().build())

        if self.use_real_dig_factory:
            self.factories.append(DigFactoryBuilder().build())

        if self.use_real_trapping_factory:
            self.factories.append(TrappingFactoryBuilder().build())

        action_factory = ActionFactory(self.model,
                                       self.factories)
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

        self.effect_factory = None
        self.dying_rules = Dying()

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

        self.spell_factory = None
        self.use_real_spell_factory = False
        self.effects_factory = None
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

class MitosisFactoryBuilder():
    """
    Builder for mitosis factory
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.character_generator = None
        self.character_limit = 30
        self.rng = Random()
        self.dying_rules = Dying()
        self.use_real_dying_rules = False

    def with_character_limit(self, character_limit):
        """
        Configure maximum amount of character at any given time
        """
        self.character_limit = character_limit
        return self

    def with_character_generator(self, generator):
        """
        Configure character generator to use
        """
        self.character_generator = generator
        return self

    def with_random_number_generator(self, rng):
        """
        Configure random number generator to use
        """
        self.rng = rng

    def with_dying_rules(self, dying_rules=None):
        """
        Configure rules for dying
        """
        if dying_rules:
            self.dying_rules = dying_rules
        else:
            self.dying_rules = Dying()

        return self

    def build(self):
        """
        Builds mitosis factory
        """
        return MitosisFactory(character_generator=self.character_generator,
                              character_limit=self.character_limit,
                              rng=self.rng,
                              dying_rules=self.dying_rules)

class MetamorphosisFactoryBuilder():
    """
    Builder for metamorphosis factory
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.character_generator = None
        self.rng = Random()

    def with_character_generator(self, generator):
        """
        Configure character generator to use
        """
        self.character_generator = generator
        return self

    def with_random_number_generator(self, rng):
        """
        Configure random number generator to use
        """
        self.rng = rng
        return self

    def build(self):
        """
        Builds metamorphosis factory
        """
        return MetamorphosisFactory(character_generator=self.character_generator,
                                    rng=self.rng)

class DigFactoryBuilder():
    """
    Builder for dig factory
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.rng = Random()

    def with_random_number_generator(rng):
        """
        Configure random number generator to use
        """
        self.rng = rng
        return self

    def build(self):
        """
        Builds dig factory
        """
        return DigFactory(self.rng)


class TrappingFactoryBuilder():
    """
    Builder for trapping factory
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        
        self.trap_creator = None

    def with_trap_creator(self, trap_creator):
        """
        Configure used trap creator
        """
        self.trap_creator = trap_creator

        return self

    def build(self):
        """
        Builds trapping factory
        """
        return TrappingFactory(self.trap_creator)

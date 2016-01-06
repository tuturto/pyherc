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
Configuration for pyherc
"""
import random
from functools import partial

from pyherc.generators import (generate_creature, get_effect_creator,
                               ItemConfigurations, ItemGenerator,
                               SpellGenerator, get_trap_creator)
from pyherc.generators.level.old_config import LevelGeneratorFactoryConfig
from pyherc.generators.level.generator import LevelGeneratorFactory
from pyherc.generators.level import PortalAdderFactory, new_dungeon, merge_level
from pyherc.generators.level import portals
from pyherc.ports import set_action_factory
from pyherc.rules import Dying, RulesEngine
from pyherc.rules.combat import RangedCombatFactory
from pyherc.rules.combat.factories import (AttackFactory, MeleeCombatFactory,
                                           UnarmedCombatFactory)
from pyherc.rules.consume.factories import DrinkFactory
from pyherc.rules.digging.factories import DigFactory
from pyherc.rules.inventory.equip import EquipFactory
from pyherc.rules.inventory.factories import (DropFactory, InventoryFactory,
                                              PickUpFactory)
from pyherc.rules.inventory.unequip import UnEquipFactory
from pyherc.rules.mitosis.factory import MitosisFactory
from pyherc.rules.metamorphosis.factory import MetamorphosisFactory
from pyherc.rules.magic import SpellCastingFactory
from pyherc.rules.moving.factories import MoveFactory
from pyherc.rules.trapping.factory import TrappingFactory
from pyherc.rules.public import ActionFactory
from pyherc.rules.waiting import WaitFactory


class Configuration():
    """
    Configuration object for Herculeum
    """
    def __init__(self, model):
        """
        Default constructor

        Args:
            model: Model to register with factories
        """
        super().__init__()
        self.resolution = None
        self.full_screen = None
        self.caption = None
        self.action_factory = None
        self.item_generator = None
        self.creature_generator = None
        self.player_generator = None
        self.trap_generator = None
        self.level_generator_factory = None
        self.level_size = None
        self.model = model
        self.rng = random.Random()
        self.rules_engine = None

    def initialise(self, context):
        """
        Initialises configuration
        """
        self.level_size = (79, 20)

        self.initialise_generators(context)
        self.initialise_level_generators(context)
        self.initialise_factories(context)

    def initialise_factories(self, context):
        """
        Initialises action factory, sub factories and various generators
        """
        dying_rules = Dying()

        move_factory = MoveFactory(self.level_generator_factory,
                                   dying_rules)

        effect_config = {}
        configurators = self.get_configurators(context.config_package,
                                               'init_effects')

        for configurator in configurators:
            effects = configurator(context)
            for effect in effects:
                effect_config[effect[0]] = effect[1]

        effect_factory = get_effect_creator(effect_config)

        unarmed_combat_factory = UnarmedCombatFactory(effect_factory,
                                                      dying_rules)
        melee_combat_factory = MeleeCombatFactory(effect_factory,
                                                  dying_rules)
        ranged_combat_factory = RangedCombatFactory(effect_factory,
                                                    dying_rules)
        attack_factory = AttackFactory([unarmed_combat_factory,
                                        melee_combat_factory,
                                        ranged_combat_factory])

        drink_factory = DrinkFactory(effect_factory,
                                     dying_rules)

        inventory_factory = InventoryFactory([PickUpFactory(),
                                              DropFactory(),
                                              EquipFactory(),
                                              UnEquipFactory()])

        wait_factory = WaitFactory()

        spell_factory = SpellGenerator()

        spell_casting_factory = SpellCastingFactory(spell_factory,
                                                    effect_factory,
                                                    dying_rules)

        mitosis_factory = MitosisFactory(self.creature_generator,
                                         self.rng,
                                         60,
                                         dying_rules)

        metamorphosis_factory = MetamorphosisFactory(self.creature_generator,
                                                     self.rng)

        dig_factory = DigFactory(self.rng)

        trapping_factory = TrappingFactory(self.trap_generator)

        self.action_factory = ActionFactory(self.model,
                                            [move_factory,
                                             attack_factory,
                                             drink_factory,
                                             inventory_factory,
                                             wait_factory,
                                             spell_casting_factory,
                                             mitosis_factory,
                                             metamorphosis_factory,
                                             dig_factory,
                                             trapping_factory])

        set_action_factory(self.action_factory)

        self.rules_engine = RulesEngine(self.action_factory,
                                        dying_rules)

    def get_creature_config(self, context):
        """
        Load creature configuration

        :param level_config: namespace of configurations
        :type level_config: Package
        :returns: configuration for creatures
        :rtype: CreatureConfigurations
        """
        config = {}

        configurators = self.get_configurators(context.config_package,
                                               'init_creatures')

        for configurator in configurators:
            creatures = configurator(context)
            for creature in creatures:
                config[creature['\ufdd0:name']] = creature

        return config

    def get_player_config(self, context):
        """
        Load player configuration

        :param level_config: namespace of configurations
        :type level_config: Package
        :returns: configuration for player characters
        :rtype: CreatureConfigurations

        .. versionadded:: 0.8
        """
        config = {}

        configurators = self.get_configurators(context.config_package,
                                               'init_players')

        for configurator in configurators:
            creatures = configurator(context)
            for creature in creatures:
                config[creature['\ufdd0:name']] = creature

        return config

    def get_item_config(self, context):
        """
        Load item configuration

        :param level_config: namespace of configurations
        :type level_config: Package
        :returns: configuration for items
        :rtype: ItemConfigurations
        """
        config = ItemConfigurations(self.rng)

        configurators = self.get_configurators(context.config_package,
                                               'init_items')

        for configurator in configurators:
            items = configurator(context)
            for item in items:
                config.add_item(item)

        return config

    def get_configurators(self, location, function_name):
        """
        Get functions to configure given sub-system
        """

        config_modules = map(lambda x: getattr(location, x),
                             filter(lambda x: x[0] != '_',
                                    dir(location)))
        configurators = map(lambda x: getattr(x, function_name),
                            filter(lambda y: hasattr(y, function_name),
                                   config_modules))

        return configurators

    def initialise_generators(self, context):
        """
        Initialise generators
        """
        self.item_generator = ItemGenerator(self.get_item_config(context))

        self.creature_generator = partial(generate_creature,
                                          self.get_creature_config(context),
                                          self.model,
                                          self.item_generator,
                                          self.rng)

        self.player_generator = partial(generate_creature,
                                        self.get_player_config(context),
                                        self.model,
                                        self.item_generator,
                                        self.rng)

        self.player_classes = self.get_player_config(context)

        configurators = self.get_configurators(context.config_package,
                                               'init_traps')

        traps = {}
        for configurator in configurators:
            temp_traps = traps.copy()
            temp_traps.update(configurator())
            traps = temp_traps

        self.trap_generator = get_trap_creator(traps)

    def initialise_level_generators(self, context):
        """
        Initialise level generators

        :param level_config: module containing level configurations
        :type level_config: module
        """
        config = new_dungeon()
 
        configurators = self.get_configurators(context.config_package,
                                               'init_level')

        for configurator in configurators:
            for level in configurator(self.rng,
                                      self.item_generator,
                                      self.creature_generator,
                                      self.level_size,
                                      context):
                merge_level(config, level)

        gfx_configurators = self.get_configurators(context.config_package, 
                                                   'init_graphics')
        for item in gfx_configurators:
            item(context)

        portal_config = []
        for key in config.keys():
            portal_config.extend(list(portals(config, key)))

        portal_adder_factory = PortalAdderFactory(
            portal_config,
            self.rng)

        self.level_generator_factory = LevelGeneratorFactory(
            portal_adder_factory,
            self.trap_generator,
            config,
            self.rng)

    def extend_configuration(self, config, new_config):
        """
        Sums two configurations together

        Args:
            config: config to extend
            new_config: items to add to configuration
        """
        config.room_generators.extend(new_config.room_generators)
        config.level_partitioners.extend(new_config.level_partitioners)
        config.decorators.extend(new_config.decorators)
        config.item_adders.extend(new_config.item_adders)
        config.creature_adders.extend(new_config.creature_adders)
        config.portal_adder_configurations.extend(
            new_config.portal_adder_configurations)
        config.contexts.extend(new_config.contexts)

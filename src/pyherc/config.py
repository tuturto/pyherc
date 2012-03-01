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
Configuration for herculeum
"""
import logging
import pyherc.gui.surfaceManager
from pyherc.rules.public import ActionFactory
from pyherc.rules.move.factories import MoveFactory
from pyherc.rules.move.factories import WalkFactory
from pyherc.rules.attack.factories import AttackFactory
from pyherc.rules.attack.factories import UnarmedCombatFactory
from pyherc.rules.attack.factories import MeleeCombatFactory
from pyherc.generators import ItemGenerator, CreatureGenerator
from pyherc.rules.tables import Tables

class Configuration(object):
    """
    Configuration object for Herculeum
    """
    def __init__(self, base_path, model):
        super(Configuration, self).__init__()
        self.resolution = None
        self.full_screen = None
        self.caption = None
        self.surface_manager = None
        self.action_factory = None
        self.base_path = None
        self.item_generator = None
        self.creature_generator = None
        self.tables = None
        self.base_path = base_path
        self.model = model
        self.logger = logging.getLogger('pyherc.config.Configuration')

    def initialise(self):
        """
        Initialises configuration

        Args:
            base_path: path to root of installation
        """
        self.resolution = (800, 600)
        self.full_screen = True
        self.caption = 'Herculeum'

        self.surface_manager = pyherc.gui.surfaceManager.SurfaceManager()
        self.surface_manager.loadResources(self.base_path)

        self.initialise_factories()
        self.initialise_tables()
        self.initialise_generators()

    def initialise_factories(self):
        """
        Initialises action factory, sub factories and various generators

        Args:
            model: Model to register to the factory
        """
        self.logger.info('Initialising action sub system')

        walk_factory = WalkFactory()
        move_factory = MoveFactory(walk_factory)

        unarmed_combat_factory = UnarmedCombatFactory()
        melee_combat_factory = MeleeCombatFactory()
        attack_factory = AttackFactory([
                                        unarmed_combat_factory,
                                        melee_combat_factory])

        self.action_factory = ActionFactory(
                                            self.model,
                                            [move_factory, attack_factory])

        self.logger.info('Action sub system initialised')

    def initialise_tables(self):
        """
        Initialise tables
        """
        self.logger.info('Initialising tables')
        self.tables = Tables()
        self.tables.load_tables(self.base_path)
        self.logger.info('Tables initialised')

    def initialise_generators(self):
        """
        Initialise generators
        """
        self.logger.info('Initialising generators')

        self.item_generator = ItemGenerator(self.tables)
        self.creature_generator = CreatureGenerator(self.action_factory,
                                                    self.tables)

        self.logger.info('Generators initialised')

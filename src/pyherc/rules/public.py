#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2011 Tuukka Turto
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
Public interface for action subsystem

Classes:
ActionFactory - Class used to contruct Action objects
ActionParameters - Class used to guide Action construction

AttackParameters - Class used to guide contruction of attack related actions
"""

import types
import random
from pyherc.aspects import Logged

class ActionFactory():
    """
    Object for creating actions
    """

    logged = Logged()

    @logged
    def __init__(self, model, factories):
        """
        Construct ActionFactory

        Args:
            model: model to register for the factory
            factories: a single Factory or list of Factories to use
        """
        if isinstance(factories, types.ListType):
            self.factories = factories
        else:
            self.factories = []
            self.factories.append(factories)

        self.model = model

    @logged
    def get_action(self, parameters):
        """
        Create an action

        Args:
            parameters: Parameters used to control action creation
        """
        parameters.set_model(self.model)

        factory = self.get_sub_factory(parameters)
        return factory.get_action(parameters)

    @logged
    def get_sub_factories(self):
        """
        Get all sub factories

        Returns:
            List of sub factories
        """
        return self.factories

    @logged
    def get_sub_factory(self, parameters):
        """
        Get sub factory to handle parameters

        Args:
            parameters: Parameters to use for searching the factory

        Returns:
            Sub factory if found, None otherwise
        """
        subs = [x for x in self.factories if x.can_handle(parameters)]

        if len(subs) == 1:
            return subs[0]
        else:
            return None

class ActionParameters():
    """
    Object for controlling action creation
    """
    logged = Logged()

    @logged
    def __init__(self):
        """
        Default constructor
        """
        self.action_type = 'default'
        self.model = None

    @logged
    def set_model(self, model):
        """
        Set model

        Args:
            model: Model to use
        """
        self.model = model

class AttackParameters(ActionParameters):
    """
    Object for controlling attack action creation
    """

    @Logged()
    def __init__(self, attacker, direction, attack_type,
                 random_number_generator):
        """
        Construct AttackParameters

        Args:
            attacker: Character doing an attack
            direction: Direction to attack to
            attack_type: type of attack to perform
            random_number_generator: Random number generator to use
        """
        ActionParameters.__init__(self)

        self.action_type = 'attack'
        self.attacker = attacker
        self.direction = direction
        self.attack_type = attack_type
        self.random_number_generator = random_number_generator
        self.model = None

    def __str__(self):
        """
        Get string representation of this object
        """
        return 'attack with attack type of ' + self.attack_type

class MoveParameters(ActionParameters):
    """
    Object for controlling move action creation
    """
    @Logged()
    def __init__(self, character, direction, movement_mode):
        """
        Construct move parameters

        Args:
            character: Character moving
            direction: Direction of the move
            movement_mode: Mode of movement
        """
        ActionParameters.__init__(self)

        self.action_type = 'move'
        self.character = character
        self.direction = direction
        self.movement_mode = movement_mode
        self.model = None

    def __str__(self):
        """
        Get string representation of this object
        """
        return 'move with movement mode of ' + self.movement_mode


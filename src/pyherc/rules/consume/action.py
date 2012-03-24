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
Module defining classes related to DrinkAction
"""
import logging
import pyherc.rules.time
import pyherc.rules.magic

class DrinkAction():
    """
    Action for drinking
    """
    def __init__(self, character, potion):
        """
        Default constructor

        Args:
            character: Character drinking
            potion: Item to drink
        """
        self.logger = logging.getLogger('pyherc.rules.move.action.MoveAction')
        self.character = character
        self.potion = potion
        self.model = None

    def execute(self):
        """
        Executes this Action
        """
        if self.is_legal():
            self.character.identify_item(self.potion)

            if 'on drink' in self.potion.effects.keys():
                for effect in self.potion.effects['on drink']:
                    pyherc.rules.magic.cast_effect(self.model,
                                                    self.character,
                                                    effect)
                    effect.charges = effect.charges - 1

                if self.potion.maximum_charges_left < 1:
                    self.character.inventory.remove(self.potion)

    def is_legal(self):
        """
        Check if the action is possible to perform

        Returns:
            True if action is possible, false otherwise
        """
        return True

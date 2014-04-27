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
Module defining classes related to DrinkAction
"""


class DrinkAction():
    """
    Action for drinking
    """
    def __init__(self, character, potion, effect_factory,
                 dying_rules):
        """
        Default constructor

        Args:
            character: Character drinking
            potion: Item to drink
            effect_factory: Initialised EffectsFactory
        """
        self.character = character
        self.potion = potion
        self.effect_factory = effect_factory
        self.dying_rules = dying_rules

    def execute(self):
        """
        Executes this Action
        """
        if self.is_legal():
            self.character.identify_item(self.potion)

            drink_effects = self.potion.get_effect_handles('on drink')

            if len(drink_effects) > 0:
                for effect_spec in drink_effects:
                    effect = self.effect_factory(effect_spec.effect,
                                                 target=self.character)

                    if effect.duration == 0:
                        effect.trigger(self.dying_rules)
                    else:
                        self.character.add_effect(effect)
                    effect_spec.charges = effect_spec.charges - 1

                if self.potion.maximum_charges_left < 1:
                    self.character.inventory.remove(self.potion)

    def is_legal(self):
        """
        Check if the action is possible to perform

        Returns:
            True if action is possible, false otherwise
        """
        return True

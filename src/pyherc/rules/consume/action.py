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

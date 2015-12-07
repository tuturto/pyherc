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
Public interface for consuming actions
"""

from pyherc.aspects import log_debug, log_info
from pyherc.rules.public import ActionParameters


@log_info
def drink(character, potion, action_factory):
    """
    Drink potion

    :param character: character about to drink
    :type character: Character
    :param potion: potion to drink
    :type potion: Item
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory
    """
    action = action_factory.get_action(DrinkParameters(character,
                                                       potion))
    action.execute()


class DrinkParameters(ActionParameters):
    """
    Object for controlling drink action creation
    """
    @log_debug
    def __init__(self, character, item):
        """
        Construct drink parameters

        Args:
            character: Character moving
            item: Item to drink
        """
        super().__init__()

        self.action_type = 'drink'
        self.character = character
        self.item = item
        self.model = None

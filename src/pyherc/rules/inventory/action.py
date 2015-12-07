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
Module defining classes related to inventory actions
"""
from pyherc.aspects import log_debug, log_info
from pyherc.events import new_drop_event, new_pick_up_event
from pyherc.data import remove_item, add_item
from pyherc.data.constants import Duration

class PickUpAction():
    """
    Action for picking up item

    .. versionadded:: 0.4
    """
    @log_debug
    def __init__(self, character, item):
        """
        Default constructor

        :param character: character moving
        :type character: Character
        :param item: item to pick up
        :type item: Item
        """
        super().__init__()
        self.character = character
        self.item = item

    @log_info
    def execute(self):
        """
        Executes this action
        """
        if self.is_legal():
            remove_item(self.character.level, self.item)

            if not self._merge_similar_items():
                self.character.inventory.append(self.item)
                self.item.location = ()

            self.character.raise_event(new_pick_up_event(self.character,
                                                         self.item))

        self.character.add_to_tick(Duration.fast)

    @log_debug
    def _merge_similar_items(self):
        """
        Merge similar items in character inventory

        :returns: True if item was merged, otherwise False
        :rtype: boolean
        """
        if self.item.ammunition_data is None:
            return False

        items = [x for x in self.character.inventory
                 if x.name == self.item.name]

        if len(items) == 0:
            return False

        merged_data = items[0].ammunition_data
        merged_data.count = merged_data.count + self.item.ammunition_data.count

        return True

    @log_debug
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if move is possible, false otherwise
        :rtype: Boolean
        """
        character = self.character
        item = self.item

        if character.location != item.location:
            return False

        return True


class DropAction():
    """
    Action for dropping item

    .. versionadded:: 0.5
    """
    @log_debug
    def __init__(self, character, item):
        """
        Default constructor

        :param character: character dropping item
        :type character: Character
        :param item: item to drop
        :type item: Item
        """
        super().__init__()

        self.character = character
        self.item = item

    @log_info
    def execute(self):
        """
        Executes this action
        """
        self.character.inventory.remove(self.item)
        add_item(self.character.level, self.character.location, self.item)

        self.character.add_to_tick(Duration.fast)
        self.character.raise_event(new_drop_event(self.character,
                                                  self.item))

    @log_debug
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if move is possible, false otherwise
        :rtype: Boolean
        """
        return True

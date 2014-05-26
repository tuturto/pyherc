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
Module defining classes related to inventory actions
"""
from pyherc.aspects import log_debug, log_info
from pyherc.events import DropEvent, PickUpEvent
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

            self.character.raise_event(PickUpEvent(self.character,
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
        self.character.raise_event(DropEvent(self.character,
                                             self.item))

    @log_debug
    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if move is possible, false otherwise
        :rtype: Boolean
        """
        return True

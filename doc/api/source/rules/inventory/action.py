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
Module defining classes related to inventory actions
"""
class PickUpAction(object):
    """
    Action for moving
    """
    def __init__(self, character, item):
        """
        Default constructor

        :param character: character moving
        :type character: Character
        :param item: item to pick up
        :type item: Item
        """
        self.character = character
        self.item = item

    def execute(self):
        """
        Executes this action
        """
        if self.is_legal():
            pass
        else:
            self.logger.warn('Tried to execute illegal move')
            self.character.add_to_tick(2)

    def is_legal(self):
        """
        Check if the action is possible to perform

        :returns: True if move is possible, false otherwise
        :rtype: Boolean
        """
        return True

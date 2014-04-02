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
Public interface of move package

.. versionadded:: 0.10
"""

from pyherc.aspects import log_debug, log_info
from pyherc.rules.public import ActionParameters


@log_info
def move(character, direction, action_factory):
    """
    Move character to specified direction

    :param character: character moving
    :type character: Character
    :param direction: direction to move
    :type direction: integer
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory
    """
    action = action_factory.get_action(MoveParameters(character,
                                                      direction,
                                                      'walk'))
    action.execute()


@log_debug
def is_move_legal(character, direction, movement_mode, action_factory):
    """
    Check if movement is legal

    :param character: character about to move
    :type character: Character
    :param direction: direction to move
    :type direction: integer
    :param movement_mode: mode of movement
    :type movement_mode: string
    :param action_factory: factory to create actions
    :type action_factory: ActionFactory
    :returns: True if move is legal, False otherwise
    :rtype: Boolean
    """
    action = action_factory.get_action(MoveParameters(character,
                                                      direction,
                                                      movement_mode))
    return action.is_legal()


class MoveParameters(ActionParameters):
    """
    Object for controlling move action creation
    """
    @log_debug
    def __init__(self, character, direction, movement_mode):
        """
        Construct move parameters

        Args:
            character: Character moving
            direction: Direction of the move
            movement_mode: Mode of movement
        """
        super().__init__()

        self.action_type = 'move'
        self.character = character
        self.direction = direction
        self.movement_mode = movement_mode
        self.model = None

    @log_debug
    def __str__(self):
        """
        Get string representation of this object
        """
        return 'move with movement mode of ' + self.movement_mode

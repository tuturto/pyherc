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
AI routines for skeletons
"""

from pyherc.aspects import Logged

class SkeletonWarriorAI(object):
    """
    AI for skeleton warrior

    ..versionadded:: 0.7
    """

    logged = Logged()

    @logged
    def __init__(self, character):
        """
        Default constructor

        :param character: character to connect
        :type character: Character
        """
        self.character = character

    @logged
    def act(self, model, action_factory, rng):
        """
        Trigger this AI to assess the situation and act accordingly

        :param model: model where the character is located
        :type model: Model
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory
        :param rng: random number generator
        :type rng: Random
        """
        pass

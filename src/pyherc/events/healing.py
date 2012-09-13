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
Classes for heal events
"""
from pyherc.events.event import Event
from pyherc.aspects import Logged

class HealTriggeredEvent(Event):
    """
    Event that can be used to relay information about heal being triggered

    .. versionadded:: 0.6
    """

    @Logged()
    def __init__(self, target, healing):
        """
        Default constructor

        :param target: character who is being healed
        :type target: Character
        :param healing: amount of healing
        :type healing: int
        """
        super(HealTriggeredEvent, self).__init__(event_type = 'heal triggered',
                                                 level = target.level,
                                                 location = target.location,
                                                 affected_tiles = [])
        self.target = target
        self.healing = healing

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.target:
            description = 'You feel better'
        else:
            description = '{0} feels better'.format(self.target.name)

        return description

class HealAddedEvent(Event):
    """
    Event raised when character has been cast healing

    .. versionadded:: 0.6
    """

    @Logged()
    def __init__(self, target):
        """
        Default constructor

        :param target: target of the event
        :type target: Character
        """
        super(HealAddedEvent, self).__init__(event_type = 'heal started',
                                             level = target.level,
                                             location = target.location,
                                             affected_tiles = [])
        self.target = target

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.target:
            description = 'You are being healed'
        else:
            description = '{0} is being healed'.format(self.target.name)

        return description

class HealEndedEvent(Event):
    """
    Event to signal that healing is over
    """

    @Logged()
    def __init__(self, target):
        """
        Default constructor

        :param actor: character not being healed anymore
        :type actor: Character
        """
        super(HealEndedEvent, self).__init__(event_type = 'heal ended',
                                             level = target.level,
                                             location = target.location,
                                             affected_tiles = [])
        self.target = target

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.target:
            description = 'You are no longer being healed'
        else:
            description = '{0} is no longer being healed'.format(self.target.name)

        return description

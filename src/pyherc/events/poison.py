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
Classes for poison events
"""
from pyherc.events.event import Event


class PoisonTriggeredEvent(Event):
    """
    Event that can be used to relay information about poison being triggered

    .. versionadded:: 0.4
    """
    def __init__(self, target, damage):
        """
        Default constructor

        :param target: character who is suffering of poisoning
        :type target: Character
        :param damage: amount of damage suffered
        :type damage: int
        """
        super().__init__(event_type='poison triggered',
                         level=target.level,
                         location=target.location,
                         affected_tiles=[])

        self.target = target
        self.damage = damage

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.target:
            description = 'You suffer from poison ({0} points of damage)'.format(self.damage)  # noqa
        else:
            description = '{0} suffers from poison ({1} points of damage)'.format(self.target.name,  # noqa
                                                                                  self.damage)  # noqa

        return description


class PoisonAddedEvent(Event):
    """
    Event raised when character has been poisoned

    .. versionadded:: 0.4
    """
    def __init__(self, target, effect):
        """
        Default constructor

        :param target: target of the event
        :type target: Character
        :param effect: effect being added
        :type effect: Poison
        """
        super().__init__(event_type='poisoned',
                         level=target.level,
                         location=target.location,
                         affected_tiles=[])

        self.target = target
        self.effect = effect

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.target:
            description = 'You have been poisoned'
        else:
            description = '{0} has been poisoned'.format(self.target.name)

        return description


class PoisonEndedEvent(Event):
    """
    Event to signal that poisoning is over
    """
    def __init__(self, target, effect):
        """
        Default constructor

        :param actor: character not suffering from poisoning anymore
        :type actor: Character
        :param effect: effect being removed
        :type effect: Poison
        """
        super().__init__(event_type='poison ended',
                         level=target.level,
                         location=target.location,
                         affected_tiles=[])

        self.target = target
        self.effect = effect

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.target:
            description = 'You are no longer poisoned'
        else:
            description = '{0} is no longer poisoned'.format(self.target.name)

        return description

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


class DamageTriggeredEvent(Event):
    """
    Event that can be used to relay information about damage being triggered

    .. versionadded:: 0.8
    """
    def __init__(self, target, damage, damage_type):
        """
        Default constructor

        :param target: character who is suffering of damage
        :type target: Character
        :param damage: amount of damage suffered
        :type damage: int
        :param damage_type: type of damage
        :type damage_type: string
        """
        super().__init__(event_type='damage triggered',
                         level=target.level,
                         location=target.location,
                         affected_tiles=[])

        self.target = target
        self.damage = damage
        self.damage_type = damage_type

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.target:
            description = 'You suffer from {0} damage ({1} points of damage)'.format(self.damage_type,  # noqa
                                                                                     self.damage)  # noqa
        else:
            description = '{0} suffers from {1} damage ({2} points of damage)'.format(self.target.name,  # noqa
                                                                               self.damage_type,  # noqa
                                                                               self.damage)  # noqa

        return description


class DamageAddedEvent(Event):
    """
    Event raised when character has been cast damage

    .. versionadded:: 0.8
    """
    def __init__(self, target, effect):
        """
        Default constructor

        :param target: target of the event
        :type target: Character
        :param effect: effect being added
        :type effect: Damage
        """
        super().__init__(event_type='damage started',
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
            description = 'You got hit by {0} damage'.format(self.effect.damage_type)  # noqa
        else:
            description = '{0} got hit by {1} damage'.format(self.target.name,
                                                             self.effect.damage_type)  # noqa

        return description


class DamageEndedEvent(Event):
    """
    Event to signal that damage effect is over
    """
    def __init__(self, target, effect):
        """
        Default constructor

        :param actor: character not suffering from damage anymore
        :type actor: Character
        :param effect: effect being removed
        :type effect: Damage
        """
        super().__init__(event_type='damage ended',
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
            description = 'You are no longer suffering of {0} damage'.format(self.effect.damage_type)  # noqa
        else:
            description = '{0} is no longer suffering {1} damage'.format(self.target.name,  # noqa
                                                                         self.effect.damage_type)  # noqa

        return description

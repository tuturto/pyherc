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
Classes for move events
"""
from pyherc.events.event import Event


class AttackHitEvent(Event):
    """
    Event that can be used to indicate attacking hitting

    .. versionadded:: 0.4
    """
    def __init__(self, type, attacker, target, damage, affected_tiles):
        """
        Default constructor
        """
        super().__init__(event_type='attack hit',
                         level=attacker.level,
                         location=attacker.location,
                         affected_tiles=affected_tiles)

        self.type = type
        self.attacker = attacker
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
        if point_of_view == self.attacker:
            description = 'You hit {0} ({1} points of damage)'.format(self.target.name,  # noqa
                                                     self.damage.damage_inflicted)  # noqa
        elif point_of_view == self.target:
            description = '{0} hits you ({1} points of damage)'.format(self.attacker.name,  # noqa
                                                      self.damage.damage_inflicted)  # noqa
        else:
            description = '{0} hits {1} ({2} points of damage)'.format(
                self.attacker.name,
                self.target.name,
                self.damage.damage_inflicted)

        return description


class AttackMissEvent(Event):
    """
    Event that can be used to indicate attacking missing

    .. versionadded:: 0.4
    """
    def __init__(self, type, attacker, target, affected_tiles):
        """
        Default constructor
        """
        super().__init__(event_type='attack miss',
                         level=attacker.level,
                         location=attacker.location,
                         affected_tiles=affected_tiles)

        self.type = type
        self.attacker = attacker
        self.target = target

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.attacker:
            description = 'You miss {0}'.format(self.target.name)
        elif point_of_view == self.target:
            description = '{0} misses you'.format(self.attacker.name)
        else:
            description = '{0} misses {1}'.format(self.attacker.name,
                                                  self.target.name)

        return description


class AttackNothingEvent(Event):
    """
    Event describing attack that targets nothing at all

    .. versionadded:: 0.5
    """
    def __init__(self, attacker, affected_tiles):
        """
        Default constructor
        """
        super().__init__(event_type='attack nothing',
                         level=attacker.level,
                         location=attacker.location,
                         affected_tiles=affected_tiles)

        self.attacker = attacker

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.attacker:
            description = 'You flail around, hitting nothing'
        else:
            description = '{0} flails around, hitting nothing'.format(
                self.attacker.name)

        return description

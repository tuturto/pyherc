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
Classes for move events
"""
from pyherc.events.event import Event

class AttackHitEvent(Event):
    """
    Event that can be used to relay information about moving

    .. versionadded:: 0.4
    """
    def __init__(self, level, location, type, attacker, target, damage, hit,
                 affected_tiles):
        """
        Default constructor
        """
        super(AttackHitEvent, self).__init__(event_type = 'attack hit',
                                             level = level,
                                             location = location,
                                             affected_tiles = affected_tiles)

        self.type = type
        self.attacker = attacker
        self.target = target
        self.damage = damage
        self.hit = hit

    def first_person_source(self):
        """
        Description from point of view of source

        :returns: description of the event
        :rtype: string
        """
        return 'you hit {0}'.format(self.target.name)

    def first_person_target(self):
        """
        Description from point of view of target

        :returns: description of the event
        :rtype: string
        """
        return 'you are hit'

    def third_person_source(self):
        """
        Description of the source

        :returns: description of the event
        :rtype: string
        """
        return '{0} hits'.format(self.attacker.name)

    def third_person_target(self):
        """
        Description of the target

        :returns: description of the event
        :rtype: string
        """
        return '{0} is hit'.format(self.target.name)

    def third_person(self):
        """
        Description of the event

        :returns: description of the event
        :rtype: string
        """
        return '{0} hits {1}'.format(self.attacker.name,
                                     self.target.name)

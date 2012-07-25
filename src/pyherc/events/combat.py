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
    def __init__(self, level, location, type, actor, target, damage, hit,
                 affected_tiles):
        """
        Default constructor
        """
        super(AttackHitEvent, self).__init__(event_type = 'attack hit',
                                             actor = actor,
                                             level = level,
                                             location = location,
                                             affected_tiles = affected_tiles)

        self.type = type
        self.target = target
        self.damage = damage
        self.hit = hit

    def first_person_description(self):
        """
        Description of the event in first person

        :returns: description of the event
        :rtype: string
        """
        return 'I hit {0}'.format(self.target.name)

    def second_person_description(self):
        """
        Description of the event in second person

        :returns: description of the event
        :rtype: string
        """
        return 'You hit {0}'.format(self.target.name)

    def third_person_description(self):
        """
        Description of the event in third person

        :returns: description of the event
        :rtype: string
        """
        return '{0} hits {1}'.format(self.actor.name,
                                     self.target.name)

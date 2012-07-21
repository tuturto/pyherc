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
Classes for poison events
"""
from pyherc.events.event import Event

class PoisonTriggered(Event):
    """
    Event that can be used to relay information about poison being triggered

    .. versionadded:: 0.4
    """
    def __init__(self, level, location, target, damage):
        """
        Default constructor
        """
        super(PoisonTriggered, self).__init__(level = level,
                                             location = location,
                                             affected_tiles = [])

        self.target = target
        self.damage = damage

    def event_type(self):
        """
        Type of the event

        :returns: type of the event
        :rtype: string
        """
        return 'poison triggered'

    def first_person_source(self):
        """
        Description from point of view of source

        :returns: description of the event
        :rtype: string
        """
        return ''

    def first_person_target(self):
        """
        Description from point of view of target

        :returns: description of the event
        :rtype: string
        """
        return 'poison burns in your veins'

    def third_person_source(self):
        """
        Description of the source

        :returns: description of the event
        :rtype: string
        """
        return ''

    def third_person_target(self):
        """
        Description of the target

        :returns: description of the event
        :rtype: string
        """
        return '{0} suffers from poison'.format(self.target.name)

    def third_person(self):
        """
        Description of the event

        :returns: description of the event
        :rtype: string
        """
        return '{0} suffers from poison'.format(self.target.name)

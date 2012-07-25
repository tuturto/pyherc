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

class MoveEvent(Event):
    """
    Event that can be used to relay information about moving

    .. versionadded:: 0.4
    """
    def __init__(self, actor, level, location, affected_tiles):
        """
        Default constructor
        """
        super(MoveEvent, self).__init__(event_type = 'move',
                                        actor = actor,
                                        level = level,
                                        location = location,
                                        affected_tiles = affected_tiles)

    def first_person_description(self):
        """
        Description of the event in first person

        :returns: description of the event
        :rtype: string
        """
        return 'I move'

    def second_person_description(self):
        """
        Description of the event in second person

        :returns: description of the event
        :rtype: string
        """
        return 'You move'

    def third_person_description(self):
        """
        Description of the event in third person

        :returns: description of the event
        :rtype: string
        """
        return '{0} moves'.format(self.actor.name)

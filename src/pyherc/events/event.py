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
Classes for events
"""
class Event(object):
    """
    Super class for events

    .. versionadded:: 0.4
    """
    def __init__(self, level, location, affected_tiles):
        """
        Default constructor

        :param level: level where event happened
        :type level: Level
        """
        super(Event, self).__init__()
        self.level = level
        self.location = location
        self.affected_tiles = affected_tiles

    def event_type(self):
        """
        Type of the event

        :returns: type of the event
        :rtype: string
        """
        return 'prototype'

    def first_person_source(self):
        """
        Description from point of view of source

        :returns: description of the event
        :rtype: string
        """
        return 'you do something'

    def first_person_target(self):
        """
        Description from point of view of target

        :returns: description of the event
        :rtype: string
        """
        return 'you are done something'

    def third_person_source(self):
        """
        Description of the source

        :returns: description of the event
        :rtype: string
        """
        return 'somebody does something'

    def third_person_target(self):
        """
        Description of the target

        :returns: description of the event
        :rtype: string
        """
        return 'somebody is done something'

    def third_person(self):
        """
        Description of the event

        :returns: description of the event
        :rtype: string
        """
        return 'somebody does something to someone'

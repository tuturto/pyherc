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
    def __init__(self, event_type, actor, level, location, affected_tiles):
        """
        Default constructor

        :param event_type: type of event
        :type event_type: string
        :param actor: actor of the event
        :type actor: Character
        :param level: level where event happened
        :type level: Level
        :param location: location where event happened
        :type location: (int, int)
        :param affected_tiles: tiles affected by the event
        :type affected_tiles: [(int, int)]
        """
        super(Event, self).__init__()
        self.__level = level
        self.__actor = actor
        self.__location = location
        self.__affected_tiles = affected_tiles
        self.__event_type = event_type

    def __get_event_type(self):
        """
        Type of the event

        :rtype: string
        """
        return self.__event_type

    def __get_actor(self):
        """
        Actor of the event

        :rtype: Character
        """
        return self.__actor

    def __get_affected_tiles(self):
        """
        Tiles affected by this event

        :rtype: [(int, int)]
        """
        return self.__affected_tiles

    def __get_location(self):
        """
        Location of the event

        :rtype: (int, int)
        """
        return self.__location

    def __get_level(self):
        """
        Level where event was triggered

        :rtype: Level
        """
        return self.__level

    event_type = property(__get_event_type)
    actor = property(__get_actor)
    affected_tiles = property(__get_affected_tiles)
    location = property(__get_location)
    level = property(__get_level)

    def first_person_description(self):
        """
        Description of the event in first person

        :returns: description of the event
        :rtype: string
        """
        return 'I do something'

    def second_person_description(self):
        """
        Description of the event in second person

        :returns: description of the event
        :rtype: string
        """
        return 'You do something'

    def third_person_description(self):
        """
        Description of the event in third person

        :returns: description of the event
        :rtype: string
        """
        if actor != None:
            return '{0} does something'.format(self.actor.name)
        else:
            return 'somebody does something'

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
Classes for events
"""


class Event():
    """
    Super class for events

    .. versionadded:: 0.4
    """
    def __init__(self, event_type, level, location, affected_tiles):
        """
        Default constructor

        :param event_type: type of event
        :type event_type: string
        :param level: level where event happened
        :type level: Level
        :param location: location where event happened
        :type location: (int, int)
        :param affected_tiles: tiles affected by the event
        :type affected_tiles: [(int, int)]
        """
        super().__init__()
        self.__level = level
        self.__location = location
        self.__affected_tiles = affected_tiles
        self.__event_type = event_type

    def __get_event_type(self):
        """
        Type of the event

        :rtype: string
        """
        return self.__event_type

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
    affected_tiles = property(__get_affected_tiles)
    location = property(__get_location)
    level = property(__get_level)

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        return 'I do something'

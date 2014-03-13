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
Classes for events signifying an error
"""
from pyherc.events.event import Event


class ErrorEvent(Event):
    """
    Event that can be used to relay information about error

    .. versionadded:: 0.9
    """
    def __init__(self, character):
        """
        Default constructor

        :param character: character performing the erroneus action
        :type character: Character
        """
        super().__init__(event_type='error',
                         level=character.level,
                         location=character.location,
                         affected_tiles=None)

        self.character = character

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.character:
            description = 'World phases out around you for a second'
        else:
            description = '{0} is unsure about existence of world'.format(self.character.name)  # noqa

        return description

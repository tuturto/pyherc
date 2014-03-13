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
Classes for perception events
"""
from pyherc.events.event import Event


class NoticeEvent(Event):
    """
    Event that can be used to indicate character noticing something interesting

    .. versionadded:: 0.8
    """
    def __init__(self, character, target):
        """
        Default constructor
        """
        super().__init__(event_type='notice',
                         level=character.level,
                         location=character.location,
                         affected_tiles=[])

        self.character = character
        self.target = target

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.character:
            description = 'You notice {0}'.format(self.target.name)
        elif point_of_view == self.target:
            description = '{0} notices you'.format(self.character.name)
        else:
            description = '{0} notices {1}'.format(self.character.name,
                                                   self.target.name)

        return description


class LoseFocusEvent(Event):
    """
    Event that can be used to indicate losing focus

    .. versionadded:: 0.8
    """
    def __init__(self, character):
        """
        Default constructor
        """
        super().__init__(event_type='lose focus',
                         level=character.level,
                         location=character.location,
                         affected_tiles=[])

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
            description = 'You lose focus'
        else:
            description = '{0} loses focus'.format(self.character.name)

        return description

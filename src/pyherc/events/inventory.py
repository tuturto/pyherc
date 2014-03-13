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
Classes for inventory events
"""
from pyherc.events.event import Event


class PickUpEvent(Event):
    """
    Event that can be used to relay information about item being picked up

    .. versionadded:: 0.5
    """
    def __init__(self, character, item):
        """
        Default constructor

        :param character: character picking up the item
        :type character: Character
        :param item: item being picked up
        :type item: Item
        """
        super().__init__(event_type='pick up',
                         level=character.level,
                         location=character.location,
                         affected_tiles=[])

        self.character = character
        self.item = item

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.character:
            description = 'You pick up {0}'.format(self.item.name)
        else:
            description = '{0} picks up {1}'.format(self.character.name,
                                                    self.item.name)

        return description


class DropEvent(Event):
    """
    Event that can be used to relay information about item being dropped

    .. versionadded:: 0.5
    """
    def __init__(self, character, item):
        """
        Default constructor

        :param character: character dropping the item
        :type character: Character
        :param item: item being dropped
        :type item: Item
        """
        super().__init__(event_type='drop',
                         level=character.level,
                         location=character.location,
                         affected_tiles=[])

        self.character = character
        self.item = item

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.character:
            description = 'You drop {0}'.format(self.item.name)
        else:
            description = '{0} drops {1}'.format(self.character.name,
                                                 self.item.name)

        return description


class EquipEvent(Event):
    """
    Event that can be used to relay information about item being equiped

    .. versionadded:: 0.8
    """
    def __init__(self, character, item):
        """
        Default constructor

        :param character: character equiping the item
        :type character: Character
        :param item: item being equipped
        :type item: Item
        """
        super().__init__(event_type='equip',
                         level=character.level,
                         location=character.location,
                         affected_tiles=[])

        self.character = character
        self.item = item

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.character:
            description = 'You equip {0}'.format(self.item.name)
        else:
            description = '{0} equips {1}'.format(self.character.name,
                                                  self.item.name)

        return description


class UnEquipEvent(Event):
    """
    Event that can be used to relay information about item being unequiped

    .. versionadded:: 0.8
    """
    def __init__(self, character, item):
        """
        Default constructor

        :param character: character unequiping the item
        :type character: Character
        :param item: item being unequipped
        :type item: Item
        """
        super().__init__(event_type='unequip',
                         level=character.level,
                         location=character.location,
                         affected_tiles=[])

        self.character = character
        self.item = item

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.character:
            description = 'You unequip {0}'.format(self.item.name)
        else:
            description = '{0} unequips {1}'.format(self.character.name,
                                                    self.item.name)

        return description

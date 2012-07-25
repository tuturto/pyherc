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

class PoisonTriggeredEvent(Event):
    """
    Event that can be used to relay information about poison being triggered

    .. versionadded:: 0.4
    """
    def __init__(self, actor, level, location, damage):
        """
        Default constructor
        """
        super(PoisonTriggeredEvent, self).__init__(event_type = 'poison triggered',
                                                   actor = actor,
                                                   level = level,
                                                   location = location,
                                                   affected_tiles = [])

        self.damage = damage

    def first_person_description(self):
        """
        Description of the event in first person

        :returns: description of the event
        :rtype: string
        """
        return 'I suffer from poison'

    def second_person_description(self):
        """
        Description of the event in second person

        :returns: description of the event
        :rtype: string
        """
        return 'You suffer from poison'

    def third_person_description(self):
        """
        Description of the event in third person

        :returns: description of the event
        :rtype: string
        """
        return '{0} suffers from poison'.format(self.actor.name)


class PoisonAddedEvent(Event):
    """
    Event raised when character has been poisoned

    .. versionadded:: 0.4
    """
    def __init__(self, actor):
        """
        Default constructor

        :param level: level of event being triggered
        :type level: Level
        :param location: location of event being triggered
        :type location: (int, int)
        :param actor: actor of the event
        :type target: Character
        """
        super(PoisonAddedEvent, self).__init__(event_type = 'poisoned',
                                               actor = actor,
                                               level = actor.level,
                                               location = actor.location,
                                               affected_tiles = [])

    def first_person_description(self):
        """
        Description of the event in first person

        :returns: description of the event
        :rtype: string
        """
        return 'I have been poisoned'

    def second_person_description(self):
        """
        Description of the event in second person

        :returns: description of the event
        :rtype: string
        """
        return 'You have been poisoned'

    def third_person_description(self):
        """
        Description of the event in third person

        :returns: description of the event
        :rtype: string
        """
        return '{0} has been poisoned'.format(self.actor.name)

class PoisonEndedEvent(Event):
    """
    Event to signal that poisoning is over
    """
    def __init__(self, actor):
        """
        Default constructor

        :param actor: character not suffering from poisoning anymore
        :type actor: Character
        """
        super(PoisonEndedEvent, self).__init__(event_type = 'poison ended',
                                               actor = actor,
                                               level = actor.level,
                                               location = actor.location,
                                               affected_tiles = [])

    def first_person_description(self):
        """
        Description of the event in first person

        :returns: description of the event
        :rtype: string
        """
        return 'I am no longer poisoned'

    def second_person_description(self):
        """
        Description of the event in second person

        :returns: description of the event
        :rtype: string
        """
        return 'You are no longer poisoned'

    def third_person_description(self):
        """
        Description of the event in third person

        :returns: description of the event
        :rtype: string
        """
        return '{0} is no longer poisoned'.format(self.actor.name)

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
Module for poison
"""
from pyherc.aspects import Logged
from pyherc.events import PoisonTriggeredEvent, PoisonAddedEvent
from pyherc.events import PoisonEndedEvent
from pyherc.data.effects.effect import Effect

class Poison(Effect):
    """
    Class representing effects of poison
    """
    logged = Logged()

    @logged
    def __init__(self, duration, frequency, tick, damage, target):
        """
        Default constructor
        """
        super(Poison, self).__init__(duration, frequency, tick)
        self.damage = damage
        self.target = target
        self.effect_name = 'poison'

    @logged
    def do_trigger(self, dying_rules):
        """
        Triggers effects of the poison
        """
        self.target.hit_points = self.target.hit_points - self.damage

        self.target.raise_event(
                        PoisonTriggeredEvent(target = self.target,
                                             damage = self.damage))

    @logged
    def get_add_event(self):
        """
        Get event describing adding of this effect

        :returns: event describing adding of this effect
        :rtype: Event
        """
        return PoisonAddedEvent(target = self.target)

    @logged
    def get_removal_event(self):
        """
        Get event describing removal of this event

        :return: event describing removal of this event
        :rtype: Event
        """
        return PoisonEndedEvent(target = self.target)

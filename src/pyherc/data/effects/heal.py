#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Module for healing
"""
from pyherc.aspects import logged
from pyherc.data.effects.effect import Effect
from pyherc.events import HealTriggeredEvent, HealAddedEvent, HealEndedEvent

class Heal(Effect):
    """
    Class representing effects of healing
    """
    @logged
    def __init__(self, duration, frequency, tick, healing, target,
                 icon, title, description):
        """
        Default constructor
        """
        super(Heal, self).__init__(duration = duration,
                                   frequency = frequency,
                                   tick = tick,
                                   icon = icon,
                                   title = title,
                                   description = description)
        self.healing = healing
        self.target = target
        self.effect_name = 'heal'

    @logged
    def do_trigger(self, dying_rules):
        """
        Triggers effects of the healing
        """
        self.target.hit_points = self.target.hit_points + self.healing

        if self.target.hit_points > self.target.max_hp:
            self.target.hit_points = self.target.max_hp

        self.target.raise_event(
                        HealTriggeredEvent(target = self.target,
                                           healing = self.healing))

    @logged
    def get_add_event(self):
        """
        Get event describing adding of this effect

        :returns: event describing adding of this effect
        :rtype: Event
        """
        return HealAddedEvent(target = self.target,
                              effect = self)

    @logged
    def get_removal_event(self):
        """
        Get event describing removal of this event

        :return: event describing removal of this event
        :rtype: Event
        """
        return HealEndedEvent(target = self.target,
                              effect = self)

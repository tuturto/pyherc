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
Module for damage
"""
from pyherc.aspects import log_debug
from pyherc.data.effects.effect import Effect
from pyherc.events import DamageTriggeredEvent

class Damage(Effect):
    """
    Class representing effects of damage
    """
    @log_debug
    def __init__(self, duration, frequency, tick, damage, target,
                 damage_type,
                 icon, title, description):
        """
        Default constructor
        """
        super().__init__(duration = duration,
                         frequency = frequency,
                         tick = tick,
                         icon = icon,
                         title = title,
                         description = description)
        self.damage = damage
        self.damage_type = damage_type
        self.target = target

    @log_debug
    def do_trigger(self, dying_rules):
        """
        Triggers effects of the damage
        """
        self.target.hit_points = self.target.hit_points - self.damage

        self.target.raise_event(
                        DamageTriggeredEvent(target = self.target,
                                             damage = self.damage,
                                             damage_type = self.damage_type))

        dying_rules.check_dying(self.target)

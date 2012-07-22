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
from pyherc.events import PoisonTriggered
from pyherc.rules.effects.effect import Effect
from pyherc.rules.ending import check_dying

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
    def do_trigger(self):
        """
        Triggers effects of the poison
        """
        self.target.hit_points = self.target.hit_points - self.damage

        self.target.raise_event(
                        PoisonTriggered(level = self.target.level,
                                        location = self.target.location,
                                        target = self.target,
                                        damage = self.damage))

        check_dying(model = self.target.model,
                    character = self.target,
                    death_params = None)

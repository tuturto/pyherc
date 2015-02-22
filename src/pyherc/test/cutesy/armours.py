# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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
Armours for behaviour driven tests
"""

from pyherc.test.builders import ItemBuilder


def LeatherArmour():
    """
    Creates a leather armour
    """
    item = (ItemBuilder()
            .with_name('leather armour')
            .with_damage_reduction(1)
            .with_speed_modifier(1.0)
            .build())

    item.old_values = {}
    return item


def ScaleMail():
    """
    Creates a scale mail
    """
    item = (ItemBuilder()
            .with_name('scale mail')
            .with_damage_reduction(3)
            .with_speed_modifier(0.7)
            .build())

    item.old_values = {}
    return item


def PlateMail():
    """
    Creates a plate mail
    """
    item = (ItemBuilder()
            .with_name('plate mail')
            .with_damage_reduction(5)
            .with_speed_modifier(0.5)
            .build())

    item.old_values = {}
    return item

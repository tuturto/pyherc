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
Module for weapons
"""
from pyherc.test.builders import ItemBuilder


def Bow():
    """
    Creates a bow
    """
    item = (ItemBuilder()
            .with_name('bow')
            .with_damage(1, 'crushing')
            .with_required_ammunition_type('arrow')
            .build())

    return item


def Arrows():
    """
    Creates a bundle of arrows
    """
    item = (ItemBuilder()
            .with_name('arrow')
            .with_range_damage(2, 'piercing')
            .with_ammunition_type('arrow')
            .with_count(10)
            .build())

    return item


def Dagger():
    """
    Creates a dagger
    """
    item = (ItemBuilder()
            .with_name('dagger')
            .with_damage(2, 'piercing')
            .build())

    return item


def Sword():
    """
    Creates a sword
    """
    item = (ItemBuilder()
            .with_name('sword')
            .with_damage(2, 'piercing')
            .with_damage(2, 'slashing')
            .build())

    return item


def Club():
    """
    Creates a club
    """
    item = (ItemBuilder()
            .with_name('club')
            .with_damage(3, 'crushing')
            .build())

    return item

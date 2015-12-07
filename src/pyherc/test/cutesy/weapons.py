# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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


def Warhammer():
    """
    Creates a warhammer
    """
    item = (ItemBuilder()
            .with_name('warhammer')
            .with_damage(7, 'crushing')
            .with_speed(0.7)
            .build())

    return item

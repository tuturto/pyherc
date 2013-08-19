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
Package for characters
"""
from pyherc.test.builders import CharacterBuilder

def strong(character):
    """
    Modifies character to be strong

    :param character: character to modify
    :type character: Character
    """
    character.body = 10
    character.hit_points = 20
    character.maximum_hit_points = 20
    return character

def weak(character):
    """
    Modifies character to be weak

    :param character: character to modify
    :type character: Character
    """
    character.body = 2
    character.hit_points = 5
    character.maximum_hit_points = 5
    return character

def Adventurer():
    """
    Creates a adventurer character

    :returns: fully initialised adventurer
    :rtype: Character
    """
    character = (CharacterBuilder()
                    .with_hit_points(10)
                    .with_max_hp(10)
                    .with_speed(5)
                    .with_body(5)
                    .with_mind(5)
                    .with_attack(1)
                    .with_name('Adventurer')
                    .build()
                    )
    character.old_values = {}
    character.old_values['hit points'] = character.hit_points
    return character

def Wizard():
    """
    Creates a wizardcharacter

    :returns: fully initialised wizard
    :rtype: Character
    """
    character = (CharacterBuilder()
                    .with_hit_points(5)
                    .with_max_hp(5)
                    .with_spirit(20)
                    .with_max_spirit(20)
                    .with_speed(4)
                    .with_body(4)
                    .with_mind(8)
                    .with_attack(1)
                    .with_name('Wizard')
                    .build()
                    )
    character.old_values = {}
    return character

def Goblin(action = None):
    """
    Creates a goblin

    :returns: fully initialised goblin
    :rtype: Character
    """
    character = (CharacterBuilder()
                    .with_hit_points(5)
                    .with_max_hp(5)
                    .with_speed(3)
                    .with_body(3)
                    .with_attack(1)
                    .with_name('Goblin')
                    .build()
                    )
    character.old_values = {}
    if action != None:
        action(character)

    return character

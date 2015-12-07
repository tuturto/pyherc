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
Package for characters
"""
from pyherc.test.builders import CharacterBuilder
from pyherc.test.cutesy.dictionary import add_history_value


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
                 .build())
    add_history_value(character, 'hit_points')

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
                 .build())

    return character


def Goblin(action=None):
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
                 .build())

    if action is not None:
        action(character)

    return character

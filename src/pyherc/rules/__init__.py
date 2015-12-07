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

# flake8: noqa

"""
Package for rules of the game
"""
from pyherc.rules.combat.interface import attack
from pyherc.rules.consume.interface import drink
from pyherc.rules.digging.interface import is_dig_legal, dig
from pyherc.rules.inventory.interface import pick_up, drop_item
from pyherc.rules.inventory.interface import equip, unequip
from pyherc.rules.magic.interface import cast, gain_domain
from pyherc.rules.moving.interface import move, is_move_legal
from pyherc.rules.trapping.interface import (place_trap, place_natural_trap,
                                             can_place_trap,
                                             can_place_natural_trap)
from pyherc.rules.waiting.interface import wait

from .public import ActionFactory
from .public import ActionParameters
from .ending import Dying
from .engine import RulesEngine

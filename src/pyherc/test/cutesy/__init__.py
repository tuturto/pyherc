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
Package for testing dsl
"""

from .characters import Goblin, Adventurer, Wizard
from .characters import strong, weak
from .weapons import Dagger, Sword, Club, Bow, Arrows, Warhammer
from .armours import (LeatherArmour, ScaleMail, PlateMail,
                      LightBoots, HeavyBoots, IronBoots, SpeedBoots,
                      FlyingBoots)
from .items import Rune
from .dictionary import at_
from .dictionary import affect, with_, potent_poison, weak_poison
from .dictionary import carrying
from .dictionary import place, middle_of, right_of, Level
from .dictionary import make, drop, hit, wait_, gain_domain_
from .dictionary import has_dropped, has_less_hit_points
from .dictionary import cast_spell
from .dictionary import take_random_step
from .traps import pit_trap, caltrops

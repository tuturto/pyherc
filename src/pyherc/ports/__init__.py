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
Package for public ports that adapters can connect to
"""

from .consuming import is_drinking_legal, drink
from .combat import is_attack_legal, attack
from .digging import is_dig_legal, dig
from .interface import set_action_factory
from .inventory import (pick_up, is_picking_up_legal, drop_item,
                        is_dropping_item_legal, equip, is_equipping_legal,
                        unequip, is_unequipping_legal)
from .magic import (cast, is_casting_legal, gain_domain,
                    is_gaining_domain_legal)
from .metamorphosis import is_morph_legal, morph
from .mitosis import is_mitosis_legal, perform_mitosis
from .moving import is_move_legal, move
from .trapping import (is_trapping_legal, place_trap,
                       is_natural_trapping_legal, place_natural_trap)
from .waiting import is_waiting_legal, wait

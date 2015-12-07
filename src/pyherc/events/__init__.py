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
Package for events that are used to communicate between creatures and UI
"""

from .combat import (new_attack_hit_event, new_attack_miss_event,
                     new_attack_nothing_event)
from .damage import (damage_triggered, damage_added, damage_ended)
from .dig import new_dig_event
from .death import new_death_event
from .effect import new_effect_added_event, new_effect_removed_event
from .error import new_error_event
from .event import (e_event_type, e_level, e_location, e_character, e_old_spirit,
                    e_new_spirit, e_target, e_damage, e_deceased, e_new_items,
                    e_new_characters, e_item, e_new_character, e_destroyed_characters,
                    e_old_location, e_direction, e_attacker, e_old_hit_points,
                    e_new_hit_points, e_trap, empty_event, e_healing)
from .healing import (new_heal_triggered_event, new_heal_added_event,
                      new_heal_ended_event)
from .hitpoints import new_hit_points_changed_event
from .inventory import (new_pick_up_event, new_drop_event, new_equip_event,
                        new_unequip_event)
from .metamorphosis import new_metamorphosis_event
from .mitosis import new_mitosis_event
from .move import new_move_event
from .new_level import new_level_event
from .perception import new_notice_event, new_lose_focus_event
from .poison import (poison_triggered, poison_added, poison_ended)
from .spirit import new_spirit_points_changed_event
from .trap import new_trap_placed_event, damage_trap_triggered

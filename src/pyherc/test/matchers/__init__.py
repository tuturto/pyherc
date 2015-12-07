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
Package for customer pyHamcrest matchers used in testing
"""
from .action import is_legal, is_illegal
from .active_effects import has_effects, has_no_effects
from .active_effects import has_effect
from .attack_parameters import AttackActionParameterMatcher
from .character import is_dead
from .contains_creature import has_creature, is_in, is_not_in
from .effect_collection import has_effect_handle, has_effect_handles
from .event_listener import has_event_listener
from .event import has_marked_for_redrawing
from .event_parameters import EventType, event_type_of
from .inventory_parameters import DropActionParameterMatcher
from .inventory import is_wearing_armour, is_wearing_boots, does_have
from .items import does_have_item, does_not_have_item, has_damage
from .map_connectivity import is_fully_accessible
from .map_connectivity import located_in_room
from .path_finding import continuous_path
from .sections import are_not_overlapping
from .targeting import wall_target_at, void_target, void_target_at

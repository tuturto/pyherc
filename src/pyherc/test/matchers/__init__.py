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

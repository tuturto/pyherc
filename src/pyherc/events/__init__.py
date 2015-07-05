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
Package for events that are used to communicate between creatures and UI
"""

from .combat import (new_attack_hit_event, new_attack_miss_event,
                     new_attack_nothing_event)
from .damage import (new_damage_triggered_event, new_damage_added_event,
                     new_damage_ended_event)
from .dig import new_dig_event
from .death import new_death_event
from .effect import new_effect_added_event, new_effect_removed_event
from .error import new_error_event
from .event import (e_event_type, e_level, e_location, e_character, e_old_spirit,
                    e_new_spirit, e_target, e_damage, e_deceased, e_new_items,
                    e_new_characters, e_item, e_new_character, e_destroyed_characters,
                    e_old_location, e_direction)
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
from .poison import (new_poison_triggered_event, new_poison_added_event,
                    new_poison_ended_event)
from .spirit import new_spirit_points_changed_event

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Package for events that are used to communicate between creatures and UI
"""
from .event import Event
from .move import MoveEvent
from .combat import AttackHitEvent, AttackNothingEvent, AttackMissEvent
from .poison import PoisonTriggeredEvent, PoisonAddedEvent, PoisonEndedEvent
from .healing import HealTriggeredEvent, HealAddedEvent, HealEndedEvent
from .death import DeathEvent
from .inventory import PickUpEvent, DropEvent
from .hitpoints import HitPointsChangedEvent
from .damage import DamageAddedEvent, DamageTriggeredEvent, DamageEndedEvent
from .perception import LoseFocusEvent, NoticeEvent

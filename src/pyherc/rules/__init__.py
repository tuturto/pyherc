# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
Package for rules of the game
"""
from pyherc.rules.moving.interface import move, is_move_legal
from pyherc.rules.magic.interface import cast, gain_domain
from pyherc.rules.inventory.interface import pick_up, drop_item
from pyherc.rules.inventory.interface import equip, unequip
from pyherc.rules.combat.interface import attack
from pyherc.rules.consume.interface import drink
from pyherc.rules.waiting.interface import wait

from .public import ActionFactory
from .public import ActionParameters
from .ending import Dying
from .engine import RulesEngine

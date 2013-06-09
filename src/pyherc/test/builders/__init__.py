#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Package for test builders
"""
from .character import CharacterBuilder
from .item import ItemBuilder
from .effect import EffectBuilder, EffectHandleBuilder, EffectsFactoryBuilder
from .level import LevelBuilder
from .action import ActionFactoryBuilder, DrinkFactoryBuilder
from .action import SpellCastingFactoryBuilder
from .poison import PoisonBuilder
from .heal import HealBuilder
from .rules_engine import RulesEngineBuilder
from .damage import DamageBuilder
from .spells import SpellGeneratorBuilder, SpellBuilder

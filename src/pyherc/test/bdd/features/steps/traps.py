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

from pyherc.test.bdd.features.helpers import default_context, get_entity
from pyherc.test.cutesy import pit_trap
from pyherc.data import add_trap


@given('{trap_name} is next to {entity_name}')
@default_context
def impl(context, trap_name, entity_name):
    trap = pit_trap()
    trap.name = trap_name

    entity = get_entity(context, entity_name)
    add_trap(entity.level,
             (entity.location[0] + 1, entity.location[1]),
             trap)

    context.places.append(trap)

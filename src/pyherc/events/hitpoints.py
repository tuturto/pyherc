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

"""
Events for hit points
"""
from pyherc.events.event import Event


class HitPointsChangedEvent(Event):
    """
    Event to raise when hit points change

    .. versionadded:: 0.7
    """
    def __init__(self, character, old_hit_points, new_hit_points):
        """
        Default constructor
        """
        super().__init__(event_type='hit points changed',
                         level=character.level,
                         location=character.location,
                         affected_tiles=[])

        self.character = character
        self.old_hit_points = old_hit_points
        self.new_hit_points = new_hit_points

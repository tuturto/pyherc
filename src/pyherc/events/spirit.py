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
Events for spirit points
"""
from pyherc.events.event import Event


class SpiritPointsChangedEvent(Event):
    """
    Event to raise when spirit points change

    .. versionadded:: 0.10
    """
    def __init__(self, character, old_spirit, new_spirit):
        """
        Default constructor
        """
        super().__init__(event_type='spirit points changed',
                         level=character.level,
                         location=character.location,
                         affected_tiles=[])

        self.character = character
        self.spirit = old_spirit
        self.spirit = new_spirit

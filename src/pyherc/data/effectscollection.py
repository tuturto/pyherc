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
Module for effects collection
"""
class EffectsCollection(object):
    """
    Class for representing collection of effects
    """
    def __init__(self):
        """
        Default constructor
        """
        super(EffectsCollection, self).__init__()
        self.handles = {}

    def add_effect_handle(self, handle):
        """
        Add effect handle

        :param handle: effect handle to add
        :type handle: EffectHandle
        """
        handles = self.handles
        trigger = handle.trigger

        if not trigger in handles.keys():
            handles[trigger] = []
        handles[trigger].append(handle)

    def get_effect_handles(self, trigger = None):
        """
        Get effect handles

        :param trigger: optional trigger type
        :type trigger: string

        :returns: effect handles
        :rtype: [EffectHandle]
        """
        if trigger is None:
            keys = self.handles.keys()
            effects = []
            for key in self.handles:
                for handle in self.handles[key]:
                    effects.append(handle)
        else:
            if trigger in self.handles.keys():
                effects = [x for x in self.handles[trigger]]
            else:
                effects = []

        return effects

    def remove_effect_handle(self, handle):
        """
        Remove given handle

        :param handle: handle to remove
        :type handle: EffectHandle
        """
        for key, value in self.handles.items():
            if handle in value:
                value.remove(handle)

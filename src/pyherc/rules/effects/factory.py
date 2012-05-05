#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
Module for Factory for creating effects
"""
from pyherc.aspects import Logged
import copy

class EffectsFactory(object):
    """
    Factory for creating effects
    """
    logged = Logged()

    @logged
    def __init__(self, config):
        """
        Default constructor

        Args:
            config: configuration parameters for effects
        """
        super(EffectsFactory, self).__init__()
        self.effects = {}
        self.config = config

    @logged
    def add_effect(self, key, type):
        """
        Add effect to internal dictionary

        Args:
            key: name of the effect
            type: type used for effect
        """
        self.effects[key] = type

    @logged
    def create_effect(self, key, **kwargs):
        """
        Instantiates new effect with given parameters

        Args:
            key: name of the effect
            kwargs: keyword arguments, passed to the effect
        """
        type = self.effects[key]

        params = copy.deepcopy(self.config.get_configuration(key))

        if params != None:
            for kw_key in kwargs:
                params.pop(kw_key)
                params[kw_key] = kwargs[kw_key]
        else:
            params = kwargs

        return type(**params)

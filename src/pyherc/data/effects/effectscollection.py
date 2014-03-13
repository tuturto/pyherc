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
Module for effects collection
"""
import collections


class EffectsCollection():
    """
    Class for representing collection of effects

    .. versionadded:: 0.4
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.handles = {}
        self.effects = []

    def add_effect_handle(self, handle):
        """
        Add effect handle

        :param handle: effect handle to add
        :type handle: EffectHandle
        """
        assert handle is not None

        handles = self.handles
        trigger = handle.trigger

        if not trigger in handles:
            handles[trigger] = []
        handles[trigger].append(handle)

    def get_effect_handles(self, trigger=None):
        """
        Get effect handles

        :param trigger: optional trigger type
        :type trigger: string

        :returns: effect handles
        :rtype: [EffectHandle]
        """
        if trigger is None:
            effects = []
            for key in self.handles:
                for handle in self.handles[key]:
                    effects.append(handle)
        else:
            if trigger in self.handles:
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
        assert handle is not None

        for key, value in self.handles.items():
            if handle in value:
                value.remove(handle)

    def has_effect(self, effect):
        """
        Check if given type of effect exists in collection

        :param effect: effect to check
        :type effect: Effect
        """
        return effect.effect_name in [x.effect_name for x in self.effects]

    def add_effect(self, effect):
        """
        Add effect

        :param effect: effect to add
        :type effect: Effect
        """
        assert effect is not None

        self.effects.append(effect)

    def get_effects(self):
        """
        Get effects from collection

        :returns: effects
        :rtype: [Effect]
        """
        return [x for x in self.effects]

    def get_expired_effects(self):
        """
        Get expired effects

        :returns: expired effects
        :rtype: [Effect]
        """
        return [x for x in self.effects
                if x.duration is not None
                and x.duration <= 0]

    def remove_expired_effects(self):
        """
        Remove expired effects from collection
        """
        self.effects = [x for x in self.effects
                        if x.duration > 0]

    def get_charges_left(self):
        """
        Amount of charges left in collection

        :returns: amount of charges
        :rtype: [integer]
        """
        if len(self.get_effect_handles()) == 0:
            return []

        return [x.charges for x in self.get_effect_handles()]

    def get_maximum_charges_left(self):
        """
        Return highest amount of charges left in collection

        :returns: highest charge
        :rtype: integer
        """
        charges = self.get_charges_left()

        if charges is not None:
            if isinstance(charges, collections.Sequence):
                if len(charges) > 0:
                    return max(charges)
                else:
                    return None
            else:
                return charges
        else:
            return None

    def get_minimum_charges_left(self):
        """
        Return smallest amount of charges left in item

        :returns: smallest charge in collection
        :rtype: integer
        """
        charges = self.get_charges_left()

        if charges is not None:
            return min(charges)
        else:
            return None

    def _repr_pretty_(self, p, cycle):
        """
        Pretty print for IPython

        :param p: printer to write
        :param cycle: has pretty print detected a cycle?
        """
        if cycle:
            p.text('EffectsCollection(...)')
        else:
            p.text('Effects:')
            for effect in self.effects:
                p.pretty(effect)
                p.breakable()

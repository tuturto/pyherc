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
Module defining classes related to damage
"""
from pyherc.aspects import log_debug


class Damage():
    """
    Damage done in attack
    """
    @log_debug
    def __init__(self, damage):
        """
        Default constructor
        """
        super().__init__()
        self.__damage = damage
        self.damage_inflicted = 0

    @log_debug
    def apply_damage(self, target):
        """
        Applies damage to target
        :param target: target to damage
        :type target: Character
        """
        for damage in self.__damage:
            damage_type = damage[1]

            matching_modifiers = [x for x in target.get_effects()
                                  if x.effect_name == 'damage modifier'
                                  and x.damage_type == damage_type]

            self.damage_inflicted = (self.damage_inflicted +
                                     damage[0] +
                                     sum(x.modifier for x
                                         in matching_modifiers))

            if self.damage_inflicted < 1:
                self.damage_inflicted = 0

        if target.inventory.armour is not None:
            armour = target.inventory.armour.armour_data.damage_reduction
        else:
            armour = 0

        if armour < self.damage_inflicted:
            self.damage_inflicted = self.damage_inflicted - armour
        else:
            if armour < self.damage_inflicted * 2:
                self.damage_inflicted = 1
            else:
                self.damage_inflicted = 0

        target.hit_points = target.hit_points - self.damage_inflicted

    @log_debug
    def __get_damage(self):
        """
        Total damage caused

        :returns: total damage caused
        :rtype: int
        """
        return sum(x[0] for x in self.__damage)

    @log_debug
    def __get_damage_types(self):
        """
        Types of damage caused

        :return: types of damage caused
        :rtype: [string]
        """
        return [x[1] for x
                in self.__damage]

    damage = property(__get_damage)
    damage_types = property(__get_damage_types)

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

"""
Classes for magic damage
"""
from .animation import Animation
from .counters import DamageCounter
from random import Random
from PyQt4.QtCore import (QEasingCurve, QPropertyAnimation,
                          QSequentialAnimationGroup)
from herculeum.ui.gui.layers import zorder_counter
from pyherc.events import e_target, e_damage

class DamageTriggeredAnimation(Animation):
    """
    Animation for damage triggering

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.location = e_target(event).location
        self.damage = -e_damage(event)
        self.colour = 'red'
        self.offset = (0, 16)

    def trigger(self, ui):
        """
        Trigger this animation
        """
        damage_counter = DamageCounter(damage=str(self.damage),
                                       colour=self.colour,
                                       parent=ui)
        ui.view.scene().addItem(damage_counter)
        damage_counter.setZValue(zorder_counter)

        bounds = damage_counter.boundingRect()
        width = bounds.width()

        rand = Random()

        damage_counter.setPos((self.location[0] * 32
                               + 16 - (width / 2)
                               + rand.randint(-16, 16)) + self.offset[0],
                              self.location[1] * 32 + self.offset[1])

        animation = QSequentialAnimationGroup()

        moving = QPropertyAnimation(damage_counter.adapter,
                                    'y_location')
        moving.setDuration(750)
        moving.setStartValue(self.location[1] * 32 + self.offset[1])
        moving.setEndValue(self.location[1] * 32 - 32 + self.offset[1])
        curve = QEasingCurve(QEasingCurve.OutElastic)
        moving.setEasingCurve(curve)
        animation.addAnimation(moving)

        fading = QPropertyAnimation(damage_counter.adapter,
                                    'opacity')
        fading.setDuration(750)
        fading.setStartValue(1.0)
        fading.setEndValue(0.0)
        animation.addAnimation(fading)

        def clean_up():
            animation.stop()
            ui.animations.remove(animation)
            ui.view.items().remove(damage_counter)
            ui.remove_finished_animation()

        animation.finished.connect(clean_up)
        ui.animations.append(animation)

        animation.start()

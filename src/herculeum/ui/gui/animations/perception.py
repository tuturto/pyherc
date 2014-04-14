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
Classes for healing
"""
from .animation import Animation
from .counters import DamageCounter
from random import Random
from PyQt4.QtCore import (QEasingCurve, QPropertyAnimation,
                          QSequentialAnimationGroup)
from herculeum.ui.gui.layers import zorder_counter


class NoticeAnimation(Animation):
    """
    Animation for character noticing something interesting

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.location = event.character.location
        self.text = '!'
        self.colour = 'red'
        self.offset = (0, 16)

    def trigger(self, ui):
        """
        Trigger this animation
        """
        damage_counter = DamageCounter(damage=self.text,
                                       colour=self.colour,
                                       parent=ui)
        ui.view.scene().addItem(damage_counter)
        damage_counter.setZValue(zorder_counter)

        bounds = damage_counter.boundingRect()
        width = bounds.width()

        damage_counter.setPos(self.location[0] * 32 + 16
                              - (width / 2) + self.offset[0],
                              self.location[1] * 32 + self.offset[1])

        animation = QSequentialAnimationGroup()

        moving = QPropertyAnimation(damage_counter.adapter,
                                    'y_location')
        moving.setDuration(750)
        moving.setStartValue(self.location[1] * 32)
        moving.setEndValue(self.location[1] * 32 - 32)

        animation.addAnimation(moving)

        fading = QPropertyAnimation(damage_counter.adapter,
                                    'opacity')
        fading.setDuration(750)
        fading.setStartValue(1.0)
        fading.setEndValue(0.0)
        animation.addAnimation(fading)

        animation.finished.connect(ui.remove_finished_animation)
        ui.animations.append(animation)

        animation.start()


class LoseFocusAnimation(Animation):
    """
    Animation for character losing focus

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.location = event.character.location
        self.text = '?'
        self.colour = 'yellow'
        self.offset = (0, 16)

    def trigger(self, ui):
        """
        Trigger this animation
        """
        damage_counter = DamageCounter(damage=self.text,
                                       colour=self.colour,
                                       parent=ui)
        ui.view.scene().addItem(damage_counter)
        damage_counter.setZValue(zorder_counter)

        bounds = damage_counter.boundingRect()
        width = bounds.width()

        damage_counter.setPos(self.location[0] * 32 + 16
                              - (width / 2) + self.offset[0],
                              self.location[1] * 32 + self.offset[1])

        animation = QSequentialAnimationGroup()

        moving = QPropertyAnimation(damage_counter.adapter,
                                    'y_location')
        moving.setDuration(750)
        moving.setStartValue(self.location[1] * 32)
        moving.setEndValue(self.location[1] * 32 - 32)

        animation.addAnimation(moving)

        fading = QPropertyAnimation(damage_counter.adapter,
                                    'opacity')
        fading.setDuration(750)
        fading.setStartValue(1.0)
        fading.setEndValue(0.0)
        animation.addAnimation(fading)

        animation.finished.connect(ui.remove_finished_animation)
        ui.animations.append(animation)

        animation.start()
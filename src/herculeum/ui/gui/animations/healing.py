# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Classes for healing
"""
from .animation import Animation
from .counters import DamageCounter
from random import Random
from PyQt4.QtCore import (QEasingCurve, QPropertyAnimation,
                          QSequentialAnimationGroup)
from herculeum.ui.gui.layers import zorder_counter
from pyherc.events import e_target, e_healing


class HealAddedAnimation(Animation):
    """
    Animation for adding healing

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.location = e_target(event).location
        self.text = 'healing'
        self.colour = 'blue'
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

        def clean_up():
            animation.stop()
            ui.animations.remove(animation)
            ui.view.items().remove(damage_counter)
            ui.remove_finished_animation()

        animation.finished.connect(clean_up)
        ui.animations.append(animation)

        animation.start()


class HealTriggeredAnimation(Animation):
    """
    Animation for heal triggering

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.location = e_target(event).location
        self.damage = e_healing(event)
        self.colour = 'blue'
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

        ui.animations.append(animation)

        animation.start()

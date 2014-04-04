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
Classes for creating animations
"""
from random import Random

from PyQt4.QtCore import (pyqtProperty, QEasingCurve, QObject,
                          QPropertyAnimation, QSequentialAnimationGroup)
from PyQt4.QtGui import QColor, QFont, QGraphicsSimpleTextItem


class AnimationFactory():
    """
    Class for creating animations for events

    .. versionadded:: 0.12
    """
    def __init__(self):
        """
        Default constructor
        """
        self.animations = {
            'attack hit': AttackHitAnimation,
            'damage triggered': DamageTriggeredAnimation,
            'death': DeathAnimation,
            'drop': DropAnimation,
            'pick up': PickUpAnimation,
        }

    def create_animation(self, event):
        """
        Create an animation for event

        :param event: event to create animation for
        :type event: Event
        :returns: animation
        :rtype: Animation
        """
        if event.event_type in self.animations:
            return self.animations[event.event_type](event)
        else:
            return Animation(event)


class Animation():
    """
    Default animation that does nothing

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        pass

    def trigger(self, ui):
        """
        Trigger this animation
        """
        pass


class DropAnimation(Animation):
    """
    Generic animation for dropping item

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.item = event.item

    def trigger(self, ui):
        """
        Trigger this animation
        """
        ui.add_glyph(self.item, ui.scene, zorder_item)


class PickUpAnimation(Animation):
    """
    Generic animation for picking up an item

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.item = event.item

    def trigger(self, ui):
        """
        Trigger this animation
        """
        glyphs = [x for x in ui.view.items()
                  if (hasattr(x, 'entity'))
                  and (x.entity == self.item)]

        for glyph in glyphs:
            ui.view.scene().removeItem(glyph)


class DeathAnimation(Animation):
    """
    Generic dying animation

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.deceased = event.deceased

    def trigger(self, ui):
        """
        Trigger this animation
        """
        glyphs = [x for x in ui.view.items()
                  if (hasattr(x, 'entity'))
                  and (x.entity == self.deceased)]

        for glyph in glyphs:
            ui.view.scene().removeItem(glyph)

        if self.deceased == ui.model.player:
            ui.EndScreenRequested.emit()


class AttackHitAnimation(Animation):
    """
    Animation for attack hit

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.location = event.target.location
        self.damage = -event.damage.damage_inflicted
        self.colour = 'white'
        self.offset = (0, 0)

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

        animation.finished.connect(ui.remove_finished_animation)
        ui.animations.append(animation)

        animation.start()


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

        self.location = event.target.location
        self.damage = -event.damage
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

        animation.finished.connect(ui.remove_finished_animation)
        ui.animations.append(animation)

        animation.start()


zorder_item = 2
zorder_counter = 30


class DamageCounter(QGraphicsSimpleTextItem):
    """
    Counter for showing damage

    .. versionadded:: 0.6
    """
    def __init__(self, damage, colour, parent):
        """
        Default constructor
        """
        super().__init__()

        font = QFont('Helvetica',
                     12,
                     QFont.Bold,
                     False)

        self.setText(str(damage))
        self.setBrush(QColor(colour))
        self.setFont(font)

        self.adapter = DamageCounterAdapter(self, self)


class DamageCounterAdapter(QObject):
    """
    Adapter for damage counter

    .. versionadded:: 0.6
    """
    def __init__(self, parent, object_to_animate):
        """
        Default constructor
        """
        super().__init__()
        self.object_to_animate = object_to_animate

    def __get_y_location(self):
        return self.object_to_animate.y()

    def __set_y_location(self, y):
        self.object_to_animate.setY(y)

    def __get_opacity(self):
        return self.object_to_animate.opacity()

    def __set_opacity(self, opacity):
        self.object_to_animate.setOpacity(opacity)

    y_location = pyqtProperty(int, __get_y_location, __set_y_location)
    opacity = pyqtProperty(float, __get_opacity, __set_opacity)

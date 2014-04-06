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
Classes for magic damage
"""
from .animation import Animation
from .counters import MapGlyphAdapter
from PyQt4.QtCore import QPropertyAnimation, QParallelAnimationGroup
from PyQt4.QtCore import QAbstractAnimation
from PyQt4.QtGui import QTransform


class MoveAnimation(Animation):
    """
    Animation for moving

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.start = event.old_location
        self.destination = event.mover.location
        self.direction = event.direction
        self.mover = event.mover

        self.flipped = False
        self.offset = 0

    def trigger(self, ui):
        """
        Trigger this animation
        """
        glyph = [glyph for glyph in ui.scene.items()
                 if hasattr(glyph, 'entity') and glyph.entity == self.mover][0]

        if self.direction in (2, 3, 4):
            self.flipped = True
            self.offset = 32

        if self.direction in (6, 7, 8):
            self.flipped = False
            self.offset = 0

        if self.flipped:
            glyph.flipped = True
            glyph.setTransform(QTransform.fromScale(-1, 1))
        else:
            glyph.flipped = False
            glyph.setTransform(QTransform.fromScale(1, 1))

        if glyph.entity.artificial_intelligence:
            adapter = MapGlyphAdapter(ui, glyph)
        else:
            adapter = MapGlyphAdapter(ui, glyph, True)

        animation = QParallelAnimationGroup()

        move_y = QPropertyAnimation(adapter, 'y_location')
        move_y.setDuration(100)
        move_y.setStartValue(self.start[1] * 32)
        move_y.setEndValue(self.destination[1] * 32)

        move_x = QPropertyAnimation(adapter, 'x_location')
        move_x.setDuration(100)
        move_x.setStartValue(self.start[0] * 32 + self.offset)
        move_x.setEndValue(self.destination[0] * 32 + self.offset)

        animation.addAnimation(move_y)
        animation.addAnimation(move_x)

        ui.animations.append(animation)
        animation.finished.connect(ui.remove_finished_animation)

        animation.start()

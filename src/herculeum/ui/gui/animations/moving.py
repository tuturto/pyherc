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
Classes for magic damage
"""
from .animation import Animation
from .counters import MapGlyphAdapter
from PyQt4.QtCore import QPropertyAnimation, QParallelAnimationGroup
from PyQt4.QtCore import QAbstractAnimation
from PyQt4.QtGui import QTransform
from pyherc.events import e_old_location, e_character, e_direction


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

        self.start = e_old_location(event)
        self.destination = e_character(event).location
        self.direction = e_direction(event)
        self.mover = e_character(event)

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

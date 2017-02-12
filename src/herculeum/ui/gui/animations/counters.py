# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
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
Classes for damage counters
"""
from PyQt4.QtCore import pyqtProperty, QObject
from PyQt4.QtGui import QColor, QFont, QGraphicsSimpleTextItem


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


class MapGlyphAdapter(QObject):
    """
    Adapter for damage counter

    .. versionadded:: 0.12
    """
    def __init__(self, parent, object_to_animate, keep_centered = False):
        """
        Default constructor
        """
        super().__init__()
        self.view = parent.view
        self.object_to_animate = object_to_animate
        self.keep_centered = keep_centered

    def __get_y_location(self):
        return self.object_to_animate.y()

    def __set_y_location(self, y):
        self.object_to_animate.setY(y)

    def __get_x_location(self):
        return self.object_to_animate.x()

    def __set_x_location(self, x):
        self.object_to_animate.setX(x)
        if self.keep_centered:
            self._center()

    def _center(self):
        if self.object_to_animate.flipped:
            off_set = 0
        else:
            off_set = 32

        self.view.setSceneRect(self.object_to_animate.x() - 180 + off_set,
                               self.object_to_animate.y() - 180,
                               320,
                               320)

    y_location = pyqtProperty(int, __get_y_location, __set_y_location)
    x_location = pyqtProperty(int, __get_x_location, __set_x_location)

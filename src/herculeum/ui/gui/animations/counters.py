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

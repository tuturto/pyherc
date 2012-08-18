#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module for main map related functionality
"""
from PyQt4.QtGui import QMdiSubWindow, QWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtCore import QSize

class PlayMapWindow(QMdiSubWindow):
    """
    Window for displaying playing world

    .. versionadded:: 0.5
    """
    def __init__(self, parent):
        """
        Default constructor
        """
        super(PlayMapWindow, self).__init__(parent)

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this window
        """
        self.map_widget = PlayMapWidget(self)

        self.setWidget(self.map_widget)

        self.setWindowTitle('Map')

        self.resize(QSize(640, 480))

class PlayMapWidget(QWidget):
    """
    Widget for displaying playing world

    .. versionadded:: 0.5
    """
    def __init__(self, parent):
        """
        Default constructor
        """
        super(PlayMapWidget, self).__init__(parent)

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
Module for small widgets
"""

from PyQt4.QtGui import QWidget, QLCDNumber, QHBoxLayout

class HitPointsWidget(QWidget):
    """
    Widget to show hitpoints
    """
    def __init__(self, parent):
        """
        Default constructor

        :param parent: parent of this widget
        :type parent: QWidget
        """
        super(HitPointsWidget, self).__init__(parent)

        self.__counter = None
        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        layout = QHBoxLayout()

        self.counter = QLCDNumber()
        layout.addWidget(self.counter)

        self.setLayout(layout)

    def receive_update(self, event):
        """
        Receive update from entity
        """
        print event
        #self.counter.text =

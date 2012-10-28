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
Module for displaying inventory
"""
from PyQt4.QtGui import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt4.QtGui import QDockWidget, QGridLayout, QDrag, QDialog
from PyQt4.QtGui import QTextEdit,  QIcon, QPixmap, QApplication
from PyQt4.QtSvg import QSvgWidget
from PyQt4.QtCore import Qt, QMimeData, pyqtSignal
import PyQt4.QtGui
import pyherc
import pyherc.rules.items

from pyherc.data import Item

class InventoryDialog(QDialog):
    """
    Dialog to show inventory

    .. versionadded:: 0.7
    """
    def __init__(self, surface_manager, character, action_factory, parent,
                 flags):
        """
        Default constructor
        """
        super(InventoryDialog, self).__init__(parent, flags)

        self.__set_layout(surface_manager,
                          character,
                          action_factory,
                          parent)

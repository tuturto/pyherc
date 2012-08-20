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
from PyQt4.QtGui import QDockWidget, QGridLayout
import PyQt4.QtGui

class InventoryDockWidget(QDockWidget):
    """
    Dock widget for showing inventory
    """
    def __init__(self, surface_manager, parent):
        """
        Default constructor
        """
        super(InventoryDockWidget, self).__init__(parent)

        self.surface_manager = surface_manager

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.inventory = InventoryWidget(self.surface_manager,
                                         self)
        self.setWidget(self.inventory)
        self.setWindowTitle('Inventory')

class InventoryWidget(QWidget):
    """
    Widget for showing inventory
    """
    def __init__(self, surface_manager, parent):
        """
        Default constructor
        """
        super(InventoryWidget, self).__init__(parent)

        self.surface_manager = surface_manager

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setSpacing(0)

        self.items1 = ItemBox(self.surface_manager, self, 4, 8)
        self.items2 = ItemBox(self.surface_manager, self, 4, 2)

        self.vertical_layout.addWidget(self.items1)
        self.vertical_layout.addWidget(self.items2)

        self.setLayout(self.vertical_layout)

class ItemBox(QWidget):
    """
    Widget for displaying many items
    """
    def __init__(self, surface_manager, parent, width, height):
        """
        Default constructor
        """
        super(ItemBox, self).__init__(parent)

        self.surface_manager = surface_manager

        self.__set_layout(width, height)

    def __set_layout(self, width, height):
        """
        Set layout of this widget
        """
        self.rows = []

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        for y in range(0, width):
            for x in range(0, height):
                new_item = ItemGlyph(None,
                                     self.surface_manager,
                                     self)

                self.grid_layout.addWidget(new_item, x, y)

        self.setLayout(self.grid_layout)

class ItemGlyph(QWidget):
    """
    Class to display item on screen
    """
    def __init__(self, item, surface_manager, parent):
        """
        Default constructor
        """
        super(ItemGlyph, self).__init__(parent)

        self.item = item
        self.surface_manager = surface_manager

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.display = QLabel()

        if self.item != None:
            self.icon = self.surface_manager.get_icon(self.item.icon)
        else:
            #TODO: empty box
            self.icon = self.surface_manager.get_icon(0)

        self.display.setPixmap(self.icon)

        #self.setWidget(self.display)
        self.grid_layout.addWidget(self.display)
        self.setLayout(self.grid_layout)

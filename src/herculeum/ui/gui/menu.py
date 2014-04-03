#!/usr/bin/env python3
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
Module for displaying menu
"""
from herculeum.ui.gui.character import CharacterWidget
from herculeum.ui.gui.inventory import InventoryWidget
from PyQt4.QtGui import QDialog, QTabWidget, QVBoxLayout


class MenuDialog(QDialog):
    """
    Dialog to show menu

    .. versionadded:: 0.7
    """
    def __init__(self, surface_manager, character, action_factory, config,
                 parent, flags):
        """
        Default constructor
        """
        super(MenuDialog, self).__init__(parent, flags)

        self.__set_layout(surface_manager,
                          character,
                          action_factory,
                          config,
                          parent)

    def __set_layout(self, surface_manager, character, action_factory,
                     config, parent):
        """
        Set layout of this widget
        """
        self.keymap = self._construct_keymap(config)
        self.setWindowTitle('Menu')
        self.inventory = InventoryWidget(surface_manager = surface_manager,
                                         character = character,
                                         action_factory = action_factory,
                                         config = config,
                                         parent = parent)

        self.character = CharacterWidget(surface_manager = surface_manager,
                                         character = character,
                                         parent = parent)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.inventory, 'Inventory')
        self.tabs.addTab(self.character, 'Character')

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)
        self.inventory.items_carried.items[0].setFocus()

    def _construct_keymap(self, config):
        """
        Construct key map

        .. versionadded:: 0.8
        """
        keymap = {}

        for key in config.left_shoulder:
            keymap[key] = self._switch_left
        for key in config.right_shoulder:
            keymap[key] = self._switch_right
        for key in config.start:
            keymap[key] = self._menu

        return keymap

    def _switch_left(self):
        """
        Switch page to left

        .. versionadded:: 0.8
        """
        current_tab = self.tabs.currentIndex()
        if current_tab > 0:
            self.tabs.setCurrentIndex(current_tab - 1)

    def _switch_right(self):
        """
        Switch page to right

        .. versionadded:: 0.8
        """
        current_tab = self.tabs.currentIndex()
        if current_tab < self.tabs.count():
            self.tabs.setCurrentIndex(current_tab + 1)

    def _menu(self):
        """
        Process menu key

        .. versionadded:: 0.8
        """
        self.done(0)

    def keyPressEvent(self, event):
        """
        Handle keyboard events
        """
        key = event.key()

        if key in self.keymap:
            self.keymap[key]()
        else:
            super(MenuDialog, self).keyPressEvent(event)

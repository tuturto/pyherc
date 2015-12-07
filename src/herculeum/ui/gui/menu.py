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

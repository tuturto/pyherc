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
Module for inventory screen
"""

from herculeum.ui.controllers import InventoryController
from pyherc.aspects import log_debug, log_info


class InventoryScreen():
    """
    Class for displaying inventero screen

    .. versionadded:: 0.9
    """
    @log_debug
    def __init__(self, character, config, screen, action_factory,
                 parent):
        """
        Default constructor
        """
        super(InventoryScreen, self).__init__()

        self.character = character
        self.config = config
        self.screen = screen.subwin(20, 75, 2, 2)
        self.inventory_controller = InventoryController(character,
                                                        action_factory)
        self.parent = parent

        self.keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D']

    @log_debug
    def _draw_screen(self):
        """
        Update the screen
        """
        self.screen.clear()
        self.screen.border()

        for index, item in enumerate(self.character.inventory):
            if index < 15:
                column = 1
                row = 1 + index
            else:
                column = 37
                row = 1 + index - 15

            self.screen.addstr(row, column,
                               '{0} {1}'.format(self.keys[index],
                                                item.get_name(self.character,
                                                              True)))

        self.screen.refresh()

    @log_info
    def show(self):
        """
        Show inventory screen
        """
        running = 1
        self._draw_screen()

        while running == 1:
            item = None
            key = chr(self.screen.getch())
            if key in ['u', 'r', 'd', 'i']:
                self.screen.addstr(0, 2, 'select item')
                item_key = chr(self.screen.getch())
                if item_key in self.keys:
                    index = self.keys.index(item_key)
                    if index < len(self.character.inventory):
                        item = self.character.inventory[index]

                if item is not None:
                    if key == 'u':
                        self.inventory_controller.use_item(item)
                    elif key == 'r':
                        self.inventory_controller.unequip_item(item)
                    elif key == 'd':
                        self.inventory_controller.drop_item(item)
                    elif key == 'i':
                        self.screen.border()
                        self.screen.addstr(0, 2, 'press key to continue')
                        self.screen.refresh()
                        self._show_detailed_info(item, self.character)
            elif key == ' ':
                running = 0

            self._draw_screen()
            self.parent.refresh()

    @log_debug
    def _show_detailed_info(self, item, character):
        """
        Show detailed information screen for item

        :param item: item to show
        :type item: Item
        """
        new_screen = self.screen.derwin(18, 73, 1, 1)
        new_screen.clear()

        new_screen.addstr(0, 0, self.inventory_controller.item_description(item))

        new_screen.refresh()

        chr(new_screen.getch())

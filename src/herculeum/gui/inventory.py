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

from pyherc.data import Item

class InventoryDialog(QDialog):
    """
    Dialog to show inventory

    .. versionadded:: 0.6
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

    def __set_layout(self, surface_manager, character, action_factory, parent):
        """
        Set layout of this widget
        """
        self.setWindowTitle('Inventory')
        self.inventory = InventoryWidget(surface_manager = surface_manager,
                                         character = character,
                                         action_factory = action_factory,
                                         parent = parent)

        layout = QVBoxLayout()
        layout.addWidget(self.inventory)

        self.setLayout(layout)
        self.inventory.items_carried.items[0].setFocus()

    def focusNextPrevChild(self, next):
        if len([x for x in self.inventory.items_carried.items
                if x.display.objectName() == 'active_inventorybox']) > 0:
            focused = self.inventory.items_carried
        elif len([x for x in self.inventory.items_in_ground.items
                  if x.display.objectName() == 'active_inventorybox']) > 0:
            focused = self.inventory.items_in_ground.items
        else:
            focused = self.inventory.character_inventory

        if focused == self.inventory.character_inventory:
            if next == True:
                self.inventory.items_carried.focus_on_first_row(0)
            else:
                self.inventory.items_in_ground.focus_on_bottom_row(0)
        elif focused == self.inventory.items_carried:
            if next == True:
                index = self.inventory.items_carried.get_current_column()
                self.inventory.items_in_ground.focus_on_first_row(index)
            else:
                self.inventory.character_inventory.focus_on_last_item()
        else:
            if next == True:
                self.inventory.character_inventory.focus_on_first_item()
            else:
                index = self.inventory.items_in_ground.get_current_column()
                self.inventory.items_carried.focus_on_bottom_row(index)

        return True

    def keyPressEvent(self, event):
        """
        Handle keyboard
        """
        if event.key() == Qt.Key_Space:
            self.done(0)

        super(InventoryDialog, self).keyPressEvent(event)

class CharacterInventoryWidget(QWidget):
    """
    Widget to show inventory of a character

    .. versionadded:: 0.6
    """
    def __init__(self, surface_manager, character, parent):
        """
        Default constructor
        """
        super(CharacterInventoryWidget, self).__init__(parent)

        self.surface_manager = surface_manager
        self.character = character
        self.items = []

        self.__set_layout(surface_manager, character, parent)

        self.move_keys = {Qt.Key_1: 1,
                          Qt.Key_2: 1,
                          Qt.Key_3: 1,
                          Qt.Key_4: -1,
                          Qt.Key_6: 1,
                          Qt.Key_7: -1,
                          Qt.Key_8: -1,
                          Qt.Key_9: -1}

    def __set_layout(self, surface_manager, character, parent):
        """
        Set layout of this widget
        """
        main_layout = QHBoxLayout()

        left_side = QVBoxLayout()
        self.ring_slot = ItemGlyph(None,
                                   surface_manager,
                                   self,
                                   QPixmap(':ring.png'))
        self.items.append(self.ring_slot)

        self.weapon_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':inventory_sword.png'))
        self.items.append(self.weapon_slot)

        self.gloves_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':mailed-fist.png'))
        self.items.append(self.gloves_slot)

        left_side.addStretch()
        left_side.addWidget(self.ring_slot)
        left_side.addWidget(self.weapon_slot)
        left_side.addWidget(self.gloves_slot)
        left_side.addStretch()

        middle = QVBoxLayout()

        middle_top = QHBoxLayout()
        self.head_slot = ItemGlyph(None,
                                   surface_manager,
                                   self,
                                   QPixmap(':helm.png'))
        self.items.append(self.head_slot)

        self.necklace_slot = ItemGlyph(None,
                                       surface_manager,
                                       self,
                                       QPixmap(':necklace.png'))
        self.items.append(self.necklace_slot)

        middle_top.addStretch()
        middle_top.addWidget(self.head_slot)
        middle_top.addWidget(self.necklace_slot)
        middle_top.addStretch()

        middle_middle = QHBoxLayout()

        self.character_icon = QSvgWidget(':strong.svg')
        self.character_icon.setMaximumSize(150, 150)
        self.character_icon.setMinimumSize(150, 150)
        middle_middle.addWidget(self.character_icon)

        middle_bottom = QHBoxLayout()
        self.boots_slot = ItemGlyph(None,
                                    surface_manager,
                                    self,
                                    QPixmap(':boots.png'))
        self.items.append(self.boots_slot)

        self.belt_slot = ItemGlyph(None,
                                   surface_manager,
                                   self,
                                   QPixmap(':belts.png'))
        self.items.append(self.belt_slot)

        middle_bottom.addStretch()
        middle_bottom.addWidget(self.boots_slot)
        middle_bottom.addWidget(self.belt_slot)
        middle_bottom.addStretch()

        middle.addLayout(middle_top)
        middle.addLayout(middle_middle)
        middle.addLayout(middle_bottom)

        right_side = QVBoxLayout()
        self.arrows_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':arrow-cluster.png'))
        self.items.append(self.arrows_slot)

        self.shield_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':shield.png'))
        self.items.append(self.shield_slot)

        self.armour_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':breastplate.png'))
        self.items.append(self.armour_slot)

        right_side.addStretch()
        right_side.addWidget(self.arrows_slot)
        right_side.addWidget(self.shield_slot)
        right_side.addWidget(self.armour_slot)
        right_side.addStretch()

        main_layout.addLayout(left_side)
        main_layout.addLayout(middle)
        main_layout.addLayout(right_side)

        self.setLayout(main_layout)

    def show_character(self, character):
        """
        Show character

        :param character: character to show
        :type character: Character
        """
        pass
        # for each slot
        #  does character have item there?
        #   yes-> show icon of item
        #   no -> show default icon

    def keyPressEvent(self, event):
        """
        Handle keyboard events
        """
        if event.key() in (Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_6,
                           Qt.Key_7, Qt.Key_8, Qt.Key_9):
            current = [x for x in self.items
                       if x.display.objectName() == 'active_inventorybox'][0]

            index = self.items.index(current)

            new_index = index + self.move_keys[event.key()]

            if new_index < len(self.items) and new_index >= 0:
                new = self.items[new_index]
                new.setFocus(Qt.OtherFocusReason)
            else:
                if new_index < 0:
                    self.focusPreviousChild()
                else:
                    self.focusNextChild()
        elif event.key() in (Qt.Key_5, Qt.Key_Enter):
            item = [x for x in self.items
                    if x.display.objectName() == 'active_inventorybox'][0].item
            if item != None:
                if event.key() == Qt.Key_5:
                    self.ItemLeftSelected.emit(item)
                else:
                    self.ItemRightSelected.emit(item)
        else:
            super(CharacterInventoryWidget, self).keyPressEvent(event)

    def focus_on_first_item(self):
        """
        Focus on the first item
        """
        self.items[0].setFocus()

    def focus_on_last_item(self):
        """
        Focus on the last item
        """
        self.items[-1].setFocus()

class ItemDescriptionWidget(QWidget):
    """
    Widget to show item description

    .. versionadded:: 0.6
    """
    def __init__(self, parent):
        """
        Default constructor
        """
        super(ItemDescriptionWidget, self).__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)

        self.__set_layout()

    def __set_layout(self):
        """
        Sets layout of this widget
        """
        layout = QHBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def set_text(self, text):
        """
        Set text being displayed on this widget
        """
        self.text_edit.setText(text)

class InventoryWidget(QWidget):
    """
    Widget for showing inventory

    .. versionadded:: 0.5
    """
    def __init__(self, surface_manager, character, action_factory, parent):
        """
        Default constructor
        """
        super(InventoryWidget, self).__init__(parent)

        self.surface_manager = surface_manager
        self.character = character
        self.action_factory = action_factory

        self.__set_layout(surface_manager, character)

    ItemPickedUp = pyqtSignal(Item, name='ItemPickedUp')
    ItemDropped = pyqtSignal(Item, name='ItemDropped')

    def __set_layout(self, surface_manager, character):
        """
        Set layout of this widget
        """
        main_layout = QHBoxLayout()

        left_side = QVBoxLayout()
        self.character_inventory = CharacterInventoryWidget(surface_manager,
                                                            character,
                                                            self)
        self.item_description = ItemDescriptionWidget(self)
        left_side.addWidget(self.character_inventory)
        left_side.addWidget(self.item_description)

        right_side = QVBoxLayout()
        self.items_carried = ItemBox(surface_manager = surface_manager,
                                     parent = self,
                                     width = 6,
                                     height = 6)
        self.items_carried.ItemFocused.connect(self.on_item_focused)
        self.items_carried.ItemLeftSelected.connect(self.use_item)
        self.items_carried.ItemRightSelected.connect(self.drop_item)

        self.items_in_ground = ItemBox(surface_manager = surface_manager,
                                       parent = self,
                                       width = 6,
                                       height = 2)
        self.items_in_ground.ItemFocused.connect(self.on_item_focused)
        self.items_in_ground.ItemLeftSelected.connect(self.pick_up_item)

        right_side.addWidget(self.items_carried)
        right_side.addWidget(self.items_in_ground)

        main_layout.addLayout(left_side)
        main_layout.addLayout(right_side)

        self.setLayout(main_layout)

        self.update_inventory()
        self.items_carried.items[0].setFocus(Qt.OtherFocusReason)

    def update_inventory(self):
        """
        Update items being displayed

        .. versionadded:: 0.6
        """
        self.items_carried.show_items(self.character.inventory)
        items = self.character.level.get_items_at(self.character.location)
        self.items_in_ground.show_items(items)
        self.character_inventory.show_character(self.character)

    def on_item_focused(self, item):
        """
        Handle item focused

        .. versionadded:: 0.6
        """
        self.item_description.set_text(item.name)

    def pick_up_item(self, item):
        """
        Pick up item

        .. versionadded:: 0.6
        """
        self.character.pick_up(item, self.action_factory)

        self.update_inventory()
        self.ItemPickedUp.emit(item)

    def drop_item(self, item):
        """
        Drop item

        .. versionadded:: 0.6
        """
        self.character.drop_item(item, self.action_factory)

        self.update_inventory()
        self.ItemDropped.emit(item)

    def use_item(self, item):
        """
        Use item in different ways, depending on the item

        .. versionadded:: 0.6
        """
        if item.get_main_type() == 'potion':
            self.character.drink(item, self.action_factory)
        self.update_inventory()

class ItemBox(QWidget):
    """
    Widget for displaying many items

    .. versionadded:: 0.5
    """
    def __init__(self, surface_manager, parent, width, height):
        """
        Default constructor
        """
        super(ItemBox, self).__init__(parent)

        self.surface_manager = surface_manager
        self.item_width = width
        self.item_height = height

        self.__set_layout(width, height)

        self.move_keys = {Qt.Key_1: width - 1,
                          Qt.Key_2: width,
                          Qt.Key_3: width + 1,
                          Qt.Key_4: -1,
                          Qt.Key_6: 1,
                          Qt.Key_7: -width - 1,
                          Qt.Key_8: -width,
                          Qt.Key_9: -width + 1}

    ItemFocused = pyqtSignal(Item, name='ItemFocused')
    ItemLeftSelected = pyqtSignal(Item, name='ItemLeftSelected')
    ItemRightSelected = pyqtSignal(Item, name='ItemRightSelected')

    def __set_layout(self, width, height):
        """
        Set layout of this widget
        """
        self.rows = []

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.items = []

        for y in range(0, height):
            for x in range(0, width):
                new_item = ItemGlyph(None,
                                     self.surface_manager,
                                     self)

                new_item.ItemFocused.connect(self.on_item_focused)
                new_item.ItemLeftSelected.connect(self.on_item_left_selected)
                new_item.ItemRightSelected.connect(self.on_item_right_selected)
                self.grid_layout.addWidget(new_item, y, x)
                self.items.append(new_item)


        self.setLayout(self.grid_layout)

    def keyPressEvent(self, event):
        """
        Handle keyboard events

        .. versionadded:: 0.6
        """
        if event.key() in (Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_6,
                           Qt.Key_7, Qt.Key_8, Qt.Key_9):
            current = self.get_current_slot()

            index = self.items.index(current)

            new_index = index + self.move_keys[event.key()]

            if new_index < len(self.items) and new_index >= 0:
                new = self.items[new_index]
                new.setFocus(Qt.OtherFocusReason)
            else:
                if new_index >= len(self.items):
                    self.focusNextChild()
                else:
                    self.focusPreviousChild()

        elif event.key() in (Qt.Key_5, Qt.Key_Enter):
            item = self.get_current_slot().item
            if item != None:
                if event.key() == Qt.Key_5:
                    self.ItemLeftSelected.emit(item)
                else:
                    self.ItemRightSelected.emit(item)
        else:
            super(ItemBox, self).keyPressEvent(event)

    def show_items(self, items):
        """
        Show given items

        .. versionadded:: 0.6
        """
        item_count = len(items)

        for counter in range(0, item_count):
            self.items[counter].set_item(items[counter])

        for counter in range(item_count, len(self.items)):
            self.items[counter].set_item(None)

    def get_current_slot(self):
        """
        Get currently selected slot
        """
        current = [x for x in self.items
                   if x.display.objectName() == 'active_inventorybox']

        if len(current) > 0:
            return current[0]
        else:
            return None

    def get_current_column(self):
        """
        Get index of current column
        """
        slot = self.get_current_slot()

        if slot == None:
            return None

        index = self.items.index(slot)
        column = index % self.item_width

        return column

    def focus_on_first_row(self, index):
        """
        Focus on slot on first row
        """
        self.items[index].setFocus()

    def focus_on_bottom_row(self, index):
        """
        Focus on slot on last row
        """
        self.items[-self.item_width + index].setFocus()

    def on_item_left_selected(self, item):
        """
        Handle left selecting item

        .. versionadded:: 0.6
        """
        self.ItemLeftSelected.emit(item)

    def on_item_right_selected(self, item):
        """
        Handle right selecting item

        .. versionadded:: 0.6
        """
        self.ItemRightSelected.emit(item)

    def on_item_focused(self, item):
        """
        Handle item focusing

        .. versionadded:: 0.6
        """
        self.ItemFocused.emit(item)

class ItemGlyph(QWidget):
    """
    Class to display item on screen

    .. versionadded:: 0.5
    """
    def __init__(self, item, surface_manager, parent, default_icon = None):
        """
        Default constructor
        """
        super(ItemGlyph, self).__init__(parent)

        self.item = item
        self.surface_manager = surface_manager
        self.default_icon = default_icon

        self.setFocusPolicy(Qt.StrongFocus)

        self.__set_layout()

    ItemFocused = pyqtSignal(Item, name='ItemFocused')
    ItemLeftSelected = pyqtSignal(Item, name='ItemLeftSelected')
    ItemRightSelected = pyqtSignal(Item, name='ItemRightSelected')

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.display = QLabel()

        self.set_item(self.item)

        self.display.setMaximumSize(40, 40)
        self.display.setObjectName('passive_inventorybox')

        self.grid_layout.addWidget(self.display)
        self.setLayout(self.grid_layout)

    def focusInEvent(self, event):
        """
        Handle focus in

        .. versionadded:: 0.6
        """
        self.display.setObjectName('active_inventorybox')
        self.display.setStyle(QApplication.style())
        if self.item != None:
            self.ItemFocused.emit(self.item)

    def focusOutEvent(self, event):
        """
        Handle focus out

        .. versionadded:: 0.6
        """
        self.display.setObjectName('passive_inventorybox')
        self.display.setStyle(QApplication.style())

    def mousePressEvent(self, event):
        """
        Handle mouse buttons

        .. versionadded:: 0.6
        """
        if event.buttons() == Qt.LeftButton:
            if self.item != None:
                self.ItemLeftSelected.emit(self.item)
            return
        elif event.buttons() == Qt.RightButton:
            if self.item != None:
                self.ItemRightSelected.emit(self.item)
            return

    def enabled(self, enabled):
        """
        Set this control enabled or disabled

        .. versionadded:: 0.6
        """
        if enabled == True:
            self.setFocusPolicy(Qt.StrongFocus)
        else:
            self.setFocusPolicy(Qt.NoFocus)

    def set_item(self, item):
        """
        Set item to be displayed

        .. versionadded:: 0.6
        """
        self.item = item

        if item != None:
            self.icon = self.surface_manager.get_icon(item.icon)
        else:
            if self.default_icon == None:
                self.icon = QPixmap(':transparent.png')
            else:
                self.icon = self.default_icon

        self.display.setPixmap(self.icon)

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

        self.__set_layout(surface_manager, character, parent)

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
        self.ring_slot.enabled(False)
        self.weapon_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':inventory_sword.png'))
        self.weapon_slot.enabled(False)
        self.gloves_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':mailed-fist.png'))
        self.gloves_slot.enabled(False)
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
        self.head_slot.enabled(False)
        self.necklace_slot = ItemGlyph(None,
                                       surface_manager,
                                       self,
                                       QPixmap(':necklace.png'))
        self.necklace_slot.enabled(False)
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
        self.boots_slot.enabled(False)
        self.belt_slot = ItemGlyph(None,
                                   surface_manager,
                                   self,
                                   QPixmap(':belts.png'))
        self.belt_slot.enabled(False)
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
        self.arrows_slot.enabled(False)
        self.shield_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':shield.png'))
        self.shield_slot.enabled(False)
        self.armour_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':breastplate.png'))
        self.armour_slot.enabled(False)
        right_side.addStretch()
        right_side.addWidget(self.arrows_slot)
        right_side.addWidget(self.shield_slot)
        right_side.addWidget(self.armour_slot)
        right_side.addStretch()

        main_layout.addLayout(left_side)
        main_layout.addLayout(middle)
        main_layout.addLayout(right_side)

        self.setLayout(main_layout)

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
        """
        self.items_carried.show_items(self.character.inventory)
        items = self.character.level.get_items_at(self.character.location)
        self.items_in_ground.show_items(items)

    def on_item_focused(self, item):
        """
        Handle item focused
        """
        self.item_description.set_text(item.name)

    def pick_up_item(self, item):
        """
        Pick up item
        """
        self.character.pick_up(item, self.action_factory)

        self.update_inventory()
        self.ItemPickedUp.emit(item)

    def drop_item(self, item):
        """
        Drop item
        """
        self.character.drop_item(item, self.action_factory)

        self.update_inventory()
        self.ItemDropped.emit(item)

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
        """
        if event.key() in (Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_6,
                           Qt.Key_7, Qt.Key_8, Qt.Key_9):
            current = [x for x in self.items
                       if x.display.objectName() == 'active_inventorybox'][0]

            index = self.items.index(current)

            if event.key() == Qt.Key_8:
                new_index = index - self.item_width
            elif event.key() == Qt.Key_2:
                new_index = index + self.item_width
            elif event.key() == Qt.Key_4:
                new_index = index - 1
            elif event.key() == Qt.Key_6:
                new_index = index + 1
            else:
                new_index = index

            new = self.items[new_index]
            new.setFocus(Qt.OtherFocusReason)
        elif event.key() in (Qt.Key_5, Qt.Key_Enter):
            item = [x for x in self.items
                    if x.display.objectName() == 'active_inventorybox'][0].item
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
        """
        empty_icon = QPixmap(':transparent.png')

        item_count = len(items)

        for counter in range(0, item_count):
            self.items[counter].display.setPixmap(
                            self.surface_manager.get_icon(items[counter].icon))
            self.items[counter].item = items[counter]

        for counter in range(item_count, len(self.items)):
            self.items[counter].display.setPixmap(empty_icon)
            self.items[counter].item = None

    def on_item_left_selected(self, item):
        """
        Handle left selecting item
        """
        self.ItemLeftSelected.emit(item)

    def on_item_right_selected(self, item):
        """
        Handle right selecting item
        """
        self.ItemRightSelected.emit(item)

    def on_item_focused(self, item):
        """
        Handle item focusing
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

        if self.item != None:
            self.icon = self.surface_manager.get_icon(self.item.icon)
        else:
            if self.default_icon == None:
                self.icon = QPixmap(':transparent.png')
            else:
                self.icon = self.default_icon

        self.display.setPixmap(self.icon)
        self.display.setMaximumSize(40, 40)
        self.display.setObjectName('passive_inventorybox')

        self.grid_layout.addWidget(self.display)
        self.setLayout(self.grid_layout)

    def focusInEvent(self, event):
        """
        Handle focus in
        """
        self.display.setObjectName('active_inventorybox')
        self.display.setStyle(QApplication.style())
        if self.item != None:
            self.ItemFocused.emit(self.item)

    def focusOutEvent(self, event):
        """
        Handle focus out
        """
        self.display.setObjectName('passive_inventorybox')
        self.display.setStyle(QApplication.style())

    def mousePressEvent(self, event):
        """
        Handle mouse buttons
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
        """
        if enabled == True:
            self.setFocusPolicy(Qt.StrongFocus)
        else:
            self.setFocusPolicy(Qt.NoFocus)

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
from PyQt4.QtGui import QTextEdit,  QIcon, QPixmap
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
        self.weapon_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':inventory_sword.png'))
        self.gloves_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':mailed-fist.png'))
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
        self.necklace_slot = ItemGlyph(None,
                                       surface_manager,
                                       self,
                                       QPixmap(':necklace.png'))
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
        self.belt_slot = ItemGlyph(None,
                                   surface_manager,
                                   self,
                                   QPixmap(':belts.png'))
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
        self.shield_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':shield.png'))
        self.armour_slot = ItemGlyph(None,
                                     surface_manager,
                                     self,
                                     QPixmap(':breastplate.png'))
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

class InventoryDockWidget(QDockWidget):
    """
    Dock widget for showing inventory

    .. versionadded:: 0.5
    """
    def __init__(self, surface_manager, character, action_factory, parent):
        """
        Default constructor
        """
        super(InventoryDockWidget, self).__init__(parent)

        self.surface_manager = surface_manager
        self.character = character
        self.action_factory = action_factory

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.inventory = InventoryWidget(self.surface_manager,
                                         self.character,
                                         self.action_factory,
                                         self)
        self.setWidget(self.inventory)
        self.setWindowTitle('Inventory')

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

        self.items_in_ground = ItemBox(surface_manager = surface_manager,
                                       parent = self,
                                       width = 6,
                                       height = 2)
        right_side.addWidget(self.items_carried)
        right_side.addWidget(self.items_in_ground)

        main_layout.addLayout(left_side)
        main_layout.addLayout(right_side)

        self.setLayout(main_layout)

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

        self.__set_layout(width, height)

    ItemAccepted = pyqtSignal(Item, name='ItemAccepted')

    def __set_layout(self, width, height):
        """
        Set layout of this widget
        """
        self.rows = []

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.items = []

        for y in range(0, width):
            for x in range(0, height):
                new_item = ItemGlyph(None,
                                     self.surface_manager,
                                     self)

                self.grid_layout.addWidget(new_item, x, y)
                self.items.append(new_item)

        self.setAcceptDrops(True)

        self.setLayout(self.grid_layout)

    def show_items(self, items):
        """
        Show given items
        """
        empty_icon = self.surface_manager.get_icon(0)

        item_count = len(items)

        for counter in range(0, item_count):
            self.items[counter].display.setPixmap(
                            self.surface_manager.get_icon(items[counter].icon))
            self.items[counter].item = items[counter]

        for counter in range(item_count, len(self.items)):
            self.items[counter].display.setPixmap(empty_icon)
            self.items[counter].item = None


    def dragEnterEvent(self, e):
        """
        Called when object being dragged has entered

        :param e: event
        """
        e.accept()

    def dropEvent(self, e):
        """
        Called when object has been dropped

        :param e: event
        """
        item = e.source().item

        e.setDropAction(Qt.MoveAction)
        e.accept()

        self.ItemAccepted.emit(item)

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
            if self.default_icon == None:
                self.icon = QPixmap(':transparent.png')
            else:
                self.icon = self.default_icon

        self.display.setPixmap(self.icon)
        self.display.setMaximumSize(34, 34)

        self.grid_layout.addWidget(self.display)
        self.setLayout(self.grid_layout)

    def mouseMoveEvent(self, e):
        """
        Called when mouse is being moved on top of the widget

        :param e: event
        """

        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.start(Qt.MoveAction)


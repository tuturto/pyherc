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
Module for displaying inventory
"""
from herculeum.ui.controllers import InventoryController
from pyherc.data import Item, get_items
from PyQt4.QtCore import pyqtSignal, Qt
from PyQt4.QtGui import (QApplication, QFont, QGridLayout, QHBoxLayout, QLabel,
                         QPainter, QPixmap, QTextEdit, QVBoxLayout, QWidget)
from PyQt4.QtSvg import QSvgWidget


class CharacterInventoryWidget(QWidget):
    """
    Widget to show inventory of a character

    .. versionadded:: 0.6
    """
    def __init__(self, surface_manager, character, config, parent):
        """
        Default constructor
        """
        super(CharacterInventoryWidget, self).__init__(parent)

        self.surface_manager = surface_manager
        self.character = character
        self.config = config
        self.items = []
        self.head_slot = None
        self.boots_slot = None
        self.shield_slot = None
        self.weapon_slot = None
        self.character_icon = None
        self.gloves_slot = None
        self.ring_slot = None
        self.arrows_slot = None
        self.necklace_slot = None
        self.belt_slot = None
        self.armour_slot = None


        self.__set_layout(surface_manager, character, parent)
        self.keymap, self.move_keys = self._construct_keymaps(config)

    ItemFocused = pyqtSignal(Item, name='ItemFocused')
    ItemActionA = pyqtSignal(Item, name='ItemActionA')
    ItemActionB = pyqtSignal(Item, name='ItemActionB')
    ItemActionX = pyqtSignal(Item, name='ItemActionX')
    ItemActionY = pyqtSignal(Item, name='ItemActionY')

    def _construct_keymaps(self, config):
        """
        Construct keymaps from configuration

        :param config: controls configuration
        :type config: ControlsConfiguration
        :returns: keymap for widget and move keys
        :rtype: {}, {}

        .. versionadded:: 0.8
        """
        move_keys = {}
        keymap = {}

        for key in config.move_down_left:
            move_keys[key] = 1
            keymap[key] = self._move
        for key in config.move_down:
            move_keys[key] = 1
            keymap[key] = self._move
        for key in config.move_down_right:
            move_keys[key] = 1
            keymap[key] = self._move
        for key in config.move_left:
            move_keys[key] = -1
            keymap[key] = self._move
        for key in config.move_right:
            move_keys[key] = 1
            keymap[key] = self._move
        for key in config.move_up_left:
            move_keys[key] = -1
            keymap[key] = self._move
        for key in config.move_up:
            move_keys[key] = -1
            keymap[key] = self._move
        for key in config.move_up_right:
            move_keys[key] = -1
            keymap[key] = self._move

        for key in config.action_a:
            keymap[key] = self._action
        for key in config.action_b:
            keymap[key] = self._action

        return keymap, move_keys

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

    def show_character(self):
        """
        Show character
        """
        self.weapon_slot.set_item(self.character.inventory.weapon)
        self.armour_slot.set_item(self.character.inventory.armour)
        self.arrows_slot.set_item(self.character.inventory.projectiles)
        self.head_slot.set_item(self.character.inventory.helm)
        self.boots_slot.set_item(self.character.inventory.boots)
        self.shield_slot.set_item(self.character.inventory.shield)
        self.gloves_slot.set_item(self.character.inventory.gloves)
        self.ring_slot.set_item(self.character.inventory.ring)
        self.necklace_slot.set_item(self.character.inventory.necklace)
        self.belt_slot.set_item(self.character.inventory.belt)

    def _move(self, key):
        """
        Handle move keys

        .. versionadded:: 0.8
        """
        current = [x for x in self.items
                   if x.display.objectName() == 'active_inventorybox'][0]

        index = self.items.index(current)
        new_index = index + self.move_keys[key]

        if new_index < len(self.items) and new_index >= 0:
            new = self.items[new_index]
            new.setFocus(Qt.OtherFocusReason)
        else:
            if new_index < 0:
                self.focusPreviousChild()
            else:
                self.focusNextChild()

    def _action(self, key):
        """
        Handle action keys

        .. versionadded:: 0.8
        """
        item = [x for x in self.items
                if x.display.objectName() == 'active_inventorybox'][0].item
        if item != None:
            if key in self.config.action_a:
                self.ItemActionA.emit(item)
            elif key in self.config.action_b:
                self.ItemActionB.emit(item)

    def keyPressEvent(self, event): #pylint: disable-msg=C0103
        """
        Handle keyboard events
        """
        key = event.key()

        if key in self.keymap:
            self.keymap[key](key)
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

        self.text_edit = None

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
    def __init__(self, surface_manager, character, action_factory,
                 config, parent):
        """
        Default constructor
        """
        super(InventoryWidget, self).__init__(parent)

        self.surface_manager = surface_manager
        self.character = character
        self.action_factory = action_factory
        self.config = config
        self.items_carried = None
        self.items_in_ground = None
        self.item_description = None
        self.character_inventory = None

        self.inventory_controller = InventoryController(character,
                                                        action_factory)

        self.__set_layout(surface_manager, character, config)

    ItemPickedUp = pyqtSignal(Item, name='ItemPickedUp')
    ItemDropped = pyqtSignal(Item, name='ItemDropped')

    def __set_layout(self, surface_manager, character, config):
        """
        Set layout of this widget
        """
        main_layout = QHBoxLayout()

        left_side = QVBoxLayout()
        self.character_inventory = CharacterInventoryWidget(surface_manager,
                                                            character,
                                                            config,
                                                            self)
        self.character_inventory.ItemActionA.connect(self.unwield_weapon)
        self.character_inventory.ItemActionB.connect(self.unwield_weapon)

        self.item_description = ItemDescriptionWidget(self)
        left_side.addWidget(self.character_inventory)
        left_side.addWidget(self.item_description)

        right_side = QVBoxLayout()
        self.items_carried = ItemBox(surface_manager = surface_manager,
                                     config = config,
                                     parent = self,
                                     width = 6,
                                     height = 6)
        self.items_carried.ItemFocused.connect(self.on_item_focused)
        self.items_carried.ItemActionA.connect(self.use_item)
        self.items_carried.ItemActionB.connect(self.drop_item)

        self.items_in_ground = ItemBox(surface_manager = surface_manager,
                                       config = config,
                                       parent = self,
                                       width = 6,
                                       height = 2)
        self.items_in_ground.ItemFocused.connect(self.on_item_focused)
        self.items_in_ground.ItemActionA.connect(self.pick_up_item)

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
        items = get_items(self.character.level, self.character.location)
        self.items_in_ground.show_items(items)
        self.character_inventory.show_character()

    def on_item_focused(self, item):
        """
        Handle item focused

        .. versionadded:: 0.6
        """
        description = self.inventory_controller.item_description(item)
        self.item_description.set_text(description)

    def focusNextPrevChild(self, next): #pylint: disable-msg=C0103
        """
        Handle moving focus around the widget

        .. versionadded:: 0.7
        """
        if len([x for x in self.items_carried.items
                if x.display.objectName() == 'active_inventorybox']) > 0:
            focused = self.items_carried
        elif len([x for x in self.items_in_ground.items
                  if x.display.objectName() == 'active_inventorybox']) > 0:
            focused = self.items_in_ground.items
        else:
            focused = self.character_inventory

        if focused == self.character_inventory:
            if next == True:
                self.items_carried.focus_on_first_row(0)
            else:
                self.items_in_ground.focus_on_bottom_row(0)
        elif focused == self.items_carried:
            if next == True:
                index = self.items_carried.get_current_column()
                self.items_in_ground.focus_on_first_row(index)
            else:
                self.character_inventory.focus_on_last_item()
        else:
            if next == True:
                self.character_inventory.focus_on_first_item()
            else:
                index = self.items_in_ground.get_current_column()
                self.items_carried.focus_on_bottom_row(index)

        return True

    def pick_up_item(self, item):
        """
        Pick up item

        .. versionadded:: 0.6
        """
        self.inventory_controller.pick_up_item(item)
        self.update_inventory()
        self.ItemPickedUp.emit(item)

    def drop_item(self, item):
        """
        Drop item

        .. versionadded:: 0.6
        """
        self.inventory_controller.drop_item(item)
        self.update_inventory()
        self.ItemDropped.emit(item)

    def use_item(self, item):
        """
        Use item in different ways, depending on the item

        .. versionadded:: 0.6
        """
        self.inventory_controller.use_item(item)
        self.update_inventory()

    def unwield_weapon(self, item):
        """
        Unwield current weapon

        .. versionadded:: 0.6
        """
        self.inventory_controller.unequip_item(item)
        self.update_inventory()

class ItemBox(QWidget):
    """
    Widget for displaying many items

    .. versionadded:: 0.5
    """
    def __init__(self, surface_manager, config, parent, width, height):
        """
        Default constructor
        """
        super(ItemBox, self).__init__(parent)

        self.config = config
        self.surface_manager = surface_manager
        self.item_width = width
        self.item_height = height

        self.rows = None
        self.items = None
        self.grid_layout = None

        self.__set_layout(width, height)

        self.keymap, self.move_keys = self._construct_keymaps(config, width)

    ItemFocused = pyqtSignal(Item, name='ItemFocused')
    ItemActionA = pyqtSignal(Item, name='ItemActionA')
    ItemActionB = pyqtSignal(Item, name='ItemActionB')
    ItemActionX = pyqtSignal(Item, name='ItemActionX')
    ItemActionY = pyqtSignal(Item, name='ItemActionY')

    def _construct_keymaps(self, config, width):
        """
        Construct keymaps from configuration

        :param config: controls configuration
        :type config: ControlsConfiguration
        :returns: keymap for widget and move keys
        :rtype: {}, {}

        .. versionadded:: 0.8
        """
        move_keys = {}
        keymap = {}

        for key in config.move_down_left:
            move_keys[key] = width - 1
            keymap[key] = self._move
        for key in config.move_down:
            move_keys[key] = width
            keymap[key] = self._move
        for key in config.move_down_right:
            move_keys[key] = width + 1
            keymap[key] = self._move
        for key in config.move_left:
            move_keys[key] = - 1
            keymap[key] = self._move
        for key in config.move_right:
            move_keys[key] = 1
            keymap[key] = self._move
        for key in config.move_up_left:
            move_keys[key] = -width - 1
            keymap[key] = self._move
        for key in config.move_up:
            move_keys[key] = -width
            keymap[key] = self._move
        for key in config.move_up_right:
            move_keys[key] = -width + 1
            keymap[key] = self._move

        for key in config.action_a:
            keymap[key] = self._action
        for key in config.action_b:
            keymap[key] = self._action

        return keymap, move_keys

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

                self.grid_layout.addWidget(new_item, y, x)
                self.items.append(new_item)
                new_item.ItemFocused.connect(self.on_item_focused)


        self.setLayout(self.grid_layout)

    def keyPressEvent(self, event): #pylint: disable-msg=C0103
        """
        Handle keyboard events

        .. versionadded:: 0.6
        """
        key = event.key()

        if key in self.keymap:
            self.keymap[key](key)
        else:
            super(ItemBox, self).keyPressEvent(event)

    def _action(self, key):
        """
        Handle action keys

        .. versionadded:: 0.8
        """
        item = self.get_current_slot().item
        if item != None:
            if key in self.config.action_a:
                self.ItemActionA.emit(item)
            elif key in self.config.action_b:
                self.ItemActionB.emit(item)

    def _move(self, key):
        """
        Handle move keys

        .. versionadded:: 0.8
        """
        current = self.get_current_slot()

        index = self.items.index(current)

        new_index = index + self.move_keys[key]

        if new_index < len(self.items) and new_index >= 0:
            new = self.items[new_index]
            new.setFocus(Qt.OtherFocusReason)
        else:
            if new_index >= len(self.items):
                self.focusNextChild()
            else:
                self.focusPreviousChild()

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
        self.ItemActionA.emit(item)

    def on_item_right_selected(self, item):
        """
        Handle right selecting item

        .. versionadded:: 0.6
        """
        self.ItemActionB.emit(item)

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

        self.grid_layout = None
        self.display = None
        self.icon = None

        self.setFocusPolicy(Qt.StrongFocus)

        self.__set_layout()

    ItemFocused = pyqtSignal(Item, name='ItemFocused')
    ItemActionA = pyqtSignal(Item, name='ItemActionA')
    ItemActionB = pyqtSignal(Item, name='ItemActionB')
    ItemActionX = pyqtSignal(Item, name='ItemActionX')
    ItemActionY = pyqtSignal(Item, name='ItemActionY')

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

    def focusInEvent(self, event): #pylint: disable-msg=C0103
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
            if item.ammunition_data != None:
                count = item.ammunition_data.count
            else:
                count = 1

            icon = self.surface_manager.get_icon(item.icon)

            if count != 1:
                image = icon.toImage()
                painter = QPainter(image)
                painter.setPen(Qt.white)
                font = QFont('Helvetica', 180, QFont.Bold)
                painter.setFont(font)
                painter.drawText(image.rect(),
                                 Qt.AlignBottom | Qt.AlignRight,
                                 str(count))
                icon = icon.fromImage(image)
                painter = None

            self.icon = icon
        else:
            if self.default_icon == None:
                self.icon = QPixmap(':transparent.png')
            else:
                self.icon = self.default_icon

        self.display.setPixmap(self.icon)

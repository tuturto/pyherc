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

from PyQt4.QtGui import QWidget, QLabel, QDockWidget, QHBoxLayout, QVBoxLayout
from PyQt4.QtGui import QFrame, QGridLayout

class HitPointsWidget(QWidget):
    """
    Widget to show hitpoints

    .. versionadded:: 0.7
    """
    def __init__(self, parent):
        """
        Default constructor

        :param parent: parent of this widget
        :type parent: QWidget
        """
        super(HitPointsWidget, self).__init__(parent)

        self.hp = None
        self.hp_label = None
        self.mana = None
        self.mana_label = None
        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        layout = QGridLayout()

        self.hp_label = QLabel()
        self.hp_label.setText('hp: ')
        self.hp_label.setObjectName('no_border')
        self.hp = QLabel()
        self.hp.setText('0 / 0')
        self.hp.setObjectName('no_border')

        self.mana_label = QLabel()
        self.mana_label.setText('mana: ')
        self.mana_label.setObjectName('no_border')
        self.mana = QLabel()
        self.mana.setText('0 / 0')
        self.mana.setObjectName('no_border')

        layout.addWidget(self.hp_label, 0, 0)
        layout.addWidget(self.hp, 0, 1)
        layout.addWidget(self.mana_label, 1, 0)
        layout.addWidget(self.mana, 1, 1)

        self.setLayout(layout)

    def receive_update(self, event):
        """
        Receive update from entity
        """
        if event.event_type == 'hit points changed':
            self.show_hit_points(event.character)

    def show_hit_points(self, character):
        """
        Show hit points of given character

        :param character: character whose hit points to show
        :type character: Character
        """
        current_hp = character.hit_points
        max_hp = character.max_hp
        self.hp.setText(str(current_hp) + '/' + str(max_hp))

class DockingHitPointsWidget(QDockWidget):
    """
    Widget to dock and show hitpoints

    .. versionadded:: 0.7
    """
    def __init__(self, parent):
        """
        Default constructor

        :param parent: parent of this widget
        :type parent: QWidget
        """
        super(DockingHitPointsWidget, self).__init__(parent)
        self.counter = None

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.counter = HitPointsWidget(self)
        self.setWidget(self.counter)

    def receive_update(self, event):
        """
        Receive update from entity
        """
        self.counter.receive_update(event)

    def show_hit_points(self, character):
        """
        Show hit points of given character

        :param character: character whose hit points to show
        :type character: Character
        """
        self.counter.show_hit_points(character)

class ListViewItem(QWidget):
    """
    Widget to show icon, title and description in a list control

    .. versionadded:: 0.7
    """
    def __init__(self, icon = None, title = '', description = ''):
        """
        Default constructor

        :param icon: icon to show
        :type icon: QPixmap
        :param title: title to show
        :type title: string
        :param description: description to show
        :type description: string
        """
        super(ListViewItem, self).__init__()

        self._icon = None
        self._title = None
        self._description = None

        self.__set_layout(icon = icon,
                          title = title,
                          description = description)

    def __set_layout(self, icon, title, description):
        """
        Set layout of this widget
        """
        self._icon = QLabel()
        self._icon.setObjectName('no_border')
        self._title = QLabel()
        self._title.setText(title)
        self._title.setWordWrap(True)
        self._title.setObjectName('charactermenu_skill_title')
        self._description = QLabel()
        self._description.setText(description)
        self._description.setWordWrap(True)
        self._description.setObjectName('no_border')
        self._icon.setPixmap(icon)
        self._icon.setMaximumSize(32, 32)

        frame = QFrame()
        frame.setObjectName('effect')

        outer_layout = QVBoxLayout()
        frame_layout = QVBoxLayout()
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        top_layout.addWidget(self._icon)

        top_layout.addWidget(self._title)
        bottom_layout.addWidget(self._description)

        frame_layout.addLayout(top_layout)
        frame_layout.addLayout(bottom_layout)
        frame.setLayout(frame_layout)

        outer_layout.addWidget(frame)

        main_layout.addLayout(outer_layout)

        self.setLayout(main_layout)

    def __get_title(self):
        return self._title.text()

    def __get_description(self):
        return self._description.text()

    def __get_icon(self):
        return self._icon.pixmap()

    title = property(__get_title)
    description = property(__get_description)
    icon = property(__get_icon)

class ListView(QWidget):
    """
    Widget to show ListViewItems

    .. versionadded:: 0.7
    """
    def __init__(self):
        """
        Default constructor
        """
        super(ListView, self).__init__()
        self._set_layout()

    def _set_layout(self):
        """
        Set layout of this widget
        """
        layout = QVBoxLayout()
        layout.addStretch()
        self.setLayout(layout)

    def add_item(self, title, description, icon):
        """
        Add item to list view

        :param title: title to show
        :type title: string
        :param description: description to show
        :type description: string
        :param icon: icon to show
        :type icon: QPixmap
        """
        new_item = ListViewItem(title = title,
                                description = description,
                                icon = icon)
        self.layout().insertWidget(self.layout().count() - 1,
                                   new_item)

class EffectsWidget(QWidget):
    """
    Widget to show current active effects

    .. versionadded:: 0.7
    """
    def __init__(self, parent, surface_manager):
        """
        Default constructor
        """
        super(EffectsWidget, self).__init__(parent)
        self.main_layout = None
        self.surface_manager = surface_manager
        self._set_layout()

    def _set_layout(self):
        """
        Set layout of this widget
        """
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

    def receive_update(self, event):
        """
        Receive update from entity
        """
        if event.event_type in ('heal started', 'poisoned',
                                'heal ended', 'poison ended'):
            for i in range(self.layout().count()):
                self.layout().itemAt(i).widget().close()

            character = event.target
            for effect in character.get_effects():
                new_icon = QLabel()
                new_icon.setPixmap(self.surface_manager.get_icon(effect.icon))
                self.layout().insertWidget(self.layout().count() - 1,
                                       new_icon)

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

        self.__counter = None
        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        layout = QHBoxLayout()

        self.description = QLabel()
        self.description.setText('Hitpoints: ')
        self.description.setObjectName('no_border')
        self.counter = QLabel()
        self.counter.setText('0 / 0')
        self.counter.setObjectName('no_border')
        layout.addWidget(self.description)
        layout.addWidget(self.counter)
        layout.addStretch()

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
        self.counter.setText(str(current_hp) + '/' + str(max_hp))

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
        self._title = QLabel()
        self._title.setText(title)
        self._description = QLabel()
        self._description.setText(description)
        self._icon.setPixmap(icon)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QHBoxLayout()

        left_layout.addWidget(self._icon)

        right_layout.addWidget(self._title)
        right_layout.addWidget(self._description)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

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

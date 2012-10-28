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
Module for displaying character
"""
from PyQt4.QtGui import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt4.QtGui import QDockWidget, QGridLayout, QDrag, QDialog
from PyQt4.QtGui import QTextEdit,  QIcon, QPixmap, QApplication
from PyQt4.QtSvg import QSvgWidget
from PyQt4.QtCore import Qt, QMimeData, pyqtSignal
import PyQt4.QtGui
import pyherc
import pyherc.rules.items

from pyherc.data import Item

class CharacterWidget(QWidget):
    """
    Widget to show character

    .. versionadded:: 0.7
    """
    def __init__(self, surface_manager, character, parent):
        """
        Default constructor
        """
        super(CharacterWidget, self).__init__(parent)

        self.__set_layout(surface_manager,
                          character)

    def __set_layout(self, surface_manager, character):
        """
        Set layout of this widget
        """
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_top_layout = QHBoxLayout()
        left_bottom_layout = QVBoxLayout()

        icon_layout = QVBoxLayout()
        stat_layout = QVBoxLayout()

        self.body = QLabel()
        self.body.setText('Body: {0}'.format(character.body))
        self.mind = QLabel()
        self.mind.setText('Mind: {0}'.format(character.mind))
        self.finesse = QLabel()
        self.finesse.setText('Finesse: {0}'.format(character.finesse))
        self.hp = QLabel()
        self.hp.setText('Hit points: {0}/{1}'.format(character.hit_points,
                                                     character.max_hp))
        self.mana = QLabel()
        self.mana.setText('Mana: 0/0')

        stat_layout.addWidget(self.body)
        stat_layout.addWidget(self.mind)
        stat_layout.addWidget(self.finesse)
        stat_layout.addWidget(self.hp)
        stat_layout.addWidget(self.mana)

        self.character_icon = QSvgWidget(':strong.svg')
        self.character_icon.setMaximumSize(150, 150)
        self.character_icon.setMinimumSize(150, 150)
        icon_layout.addWidget(self.character_icon)

        skills = QLabel()
        skills.setText('Skills')

        right_layout.addWidget(skills)

        effects = QLabel()
        effects.setText('Effects')
        left_bottom_layout.addWidget(effects)

        left_top_layout.addLayout(icon_layout)
        left_top_layout.addLayout(stat_layout)
        left_layout.addLayout(left_top_layout)
        left_layout.addLayout(left_bottom_layout)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

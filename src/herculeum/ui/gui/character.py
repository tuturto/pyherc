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
Module for displaying character
"""
from herculeum.ui.gui.widgets import ListView
from PyQt4.QtGui import QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from PyQt4.QtSvg import QSvgWidget


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

        self.body = None
        self.finesse = None
        self.character_icon = None
        self.hp = None
        self.mind = None
        self.mana = None

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
        stat_layout = QGridLayout()

        self.body = QLabel()
        self.body.setText(str(character.body))
        self.body.setObjectName('no_border')
        self.mind = QLabel()
        self.mind.setText(str(character.mind))
        self.mind.setObjectName('no_border')
        self.finesse = QLabel()
        self.finesse.setText(str(character.finesse))
        self.finesse.setObjectName('no_border')
        self.hp = QLabel()
        self.hp.setText('{0}/{1}'.format(character.hit_points,
                                         character.max_hp))
        self.hp.setObjectName('no_border')
        self.mana = QLabel()
        self.mana.setText('0/0')
        self.mana.setObjectName('no_border')

        body_label = QLabel('Body:')
        body_label.setObjectName('no_border')
        mind_label = QLabel('Mind:')
        mind_label.setObjectName('no_border')
        finesse_label = QLabel('Finesse:')
        finesse_label.setObjectName('no_border')
        hp_label = QLabel('HP:')
        hp_label.setObjectName('no_border')
        mana_label = QLabel('Mana:')
        mana_label.setObjectName('no_border')

        stat_layout.addWidget(self.body, 0, 1)
        stat_layout.addWidget(body_label, 0, 0)
        stat_layout.addWidget(self.mind, 1, 1)
        stat_layout.addWidget(mind_label, 1, 0)
        stat_layout.addWidget(self.finesse, 2, 1)
        stat_layout.addWidget(finesse_label, 2, 0)
        stat_layout.addWidget(self.hp, 3, 1)
        stat_layout.addWidget(hp_label, 3, 0)
        stat_layout.addWidget(self.mana, 4, 1)
        stat_layout.addWidget(mana_label, 4, 0)


        self.character_icon = QSvgWidget(':strong.svg')
        self.character_icon.setMaximumSize(150, 150)
        self.character_icon.setMinimumSize(150, 150)
        icon_layout.addWidget(self.character_icon)

        skills_label = QLabel('Skills')
        skills_label.setObjectName('section_title')
        skills = ListView()

        right_layout.addWidget(skills_label)
        right_layout.addWidget(skills)

        effects_label = QLabel('Effects')
        effects_label.setObjectName('section_title')
        effects = ListView()

        for effect in character.get_effects():
            effects.add_item(title = effect.title,
                             description = effect.description,
                             icon = surface_manager.get_icon(effect.icon))

        left_bottom_layout.addWidget(effects_label)
        left_bottom_layout.addWidget(effects)

        left_top_layout.addLayout(icon_layout)
        left_top_layout.addLayout(stat_layout)
        left_layout.addLayout(left_top_layout)
        left_layout.addLayout(left_bottom_layout)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

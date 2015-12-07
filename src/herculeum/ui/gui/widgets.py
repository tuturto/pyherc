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
Module for small widgets
"""
from PyQt4.QtGui import (QDockWidget, QFrame, QGridLayout, QHBoxLayout, QLabel,
                         QVBoxLayout, QWidget)
from pyherc.events import e_event_type, e_character, e_target


class HitPointsWidget(QWidget):
    """
    Widget to show hitpoints

    .. versionadded:: 0.7
    """
    def __init__(self, parent, surface_manager):
        """
        Default constructor

        :param parent: parent of this widget
        :type parent: QWidget
        """
        super().__init__(parent)

        self.surface_manager = surface_manager
        self.hp = []
        self.spirit = []
        self.__set_layout()
        

    def __set_layout(self):
        """
        Set layout of this widget
        """
        layout = QGridLayout()
        
        for count in range(10):
            temp_hp = QLabel()
            temp_hp.setObjectName('no_border')
            temp_hp.setPixmap(self.surface_manager.get_icon('heart_red_4'))
            self.hp.append(temp_hp)

            temp_spirit = QLabel()
            temp_spirit.setObjectName('no_border')
            temp_spirit.setPixmap(self.surface_manager.get_icon('heart_blue_4'))
            self.spirit.append(temp_spirit)

            layout.addWidget(temp_hp, 0, count)
            layout.addWidget(temp_spirit, 0, 10 + count)

        self.setLayout(layout)

    def receive_update(self, event):
        """
        Receive update from entity
        """
        if e_event_type(event) == 'hit points changed':
            self.show_hit_points(e_character(event))
        elif e_event_type(event) == 'spirit points changed':
            self.show_spirit_points(e_character(event))

    def show_hit_points(self, character):
        """
        Show hit points of given character

        :param character: character whose hit points to show
        :type character: Character
        """
        current_hp = character.hit_points
        max_hp = character.max_hp
        for count, label in enumerate(self.hp):
            if count >= max_hp // 4:
                label.setPixmap(self.surface_manager.get_icon('transparent'))
            elif count == current_hp // 4:
                if current_hp % 4 == 1:
                    label.setPixmap(self.surface_manager.get_icon('heart_red_1'))
                elif current_hp % 4 == 2:
                    label.setPixmap(self.surface_manager.get_icon('heart_red_2'))
                elif current_hp % 4 == 3:
                    label.setPixmap(self.surface_manager.get_icon('heart_red_3'))
                elif current_hp % 4 == 0:
                    label.setPixmap(self.surface_manager.get_icon('heart_red_0'))
            elif count < current_hp // 4:
                label.setPixmap(self.surface_manager.get_icon('heart_red_4'))
            else:
                label.setPixmap(self.surface_manager.get_icon('heart_red_0'))

    def show_spirit_points(self, character):
        """
        Show spirit points of given character

        :param character: character whose spirit points to show
        :type character: Character

        .. versionadded:: 0.10
        """
        current_spirit = character.spirit
        max_spirit = character.max_spirit
        for count, label in enumerate(self.spirit):
            if count >= max_spirit // 4:
                label.setPixmap(self.surface_manager.get_icon('transparent'))
            elif count == current_spirit // 4:
                if current_spirit % 4 == 1:
                    label.setPixmap(self.surface_manager.get_icon('heart_blue_1'))
                elif current_spirit % 4 == 2:
                    label.setPixmap(self.surface_manager.get_icon('heart_blue_2'))
                elif current_spirit % 4 == 3:
                    label.setPixmap(self.surface_manager.get_icon('heart_blue_3'))
                elif current_spirit % 4 == 0:
                    label.setPixmap(self.surface_manager.get_icon('heart_blue_0'))
            elif count < current_spirit // 4:
                label.setPixmap(self.surface_manager.get_icon('heart_blue_4'))
            else:
                label.setPixmap(self.surface_manager.get_icon('heart_blue_0'))

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
        super().__init__(parent)
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
        super().__init__()

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
        super().__init__()
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
        super().__init__(parent)
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
        if e_event_type(event) in ('heal started', 'poisoned',
                                   'heal ended', 'poison ended',
                                   'damage started', 'damage ended'):
            for i in range(self.layout().count()):
                self.layout().itemAt(i).widget().close()

            character = e_target(event)
            for effect in character.get_effects():
                new_icon = QLabel()
                new_icon.setPixmap(self.surface_manager.get_icon(effect.icon))
                self.layout().insertWidget(self.layout().count() - 1,
                                       new_icon)

class SpellSelectorWidget(QWidget):
    """
    Widget for selecting spell

    .. versionadded:: 0.10
    """
    def __init__(self, parent, surface_manager):
        """
        Default constructor
        """
        super().__init__(parent)
        self.surface_manager = surface_manager
        self._set_layout()

    def _set_layout(self):
        """
        Set layout of this widget
        """
        self.main_layout = QHBoxLayout()
        self.icon = QLabel()
        self.main_layout.addWidget(self.icon)
        self.icon.setPixmap(self.surface_manager.get_icon('transparent'))
        self.setLayout(self.main_layout)

    def next_spell(self):
        """
        Select next spell
        """
        self.icon.setPixmap(self.surface_manager.get_icon('fire effect'))

    def previous_spell(self):
        """
        Select previous spell
        """
        self.icon.setPixmap(self.surface_manager.get_icon('minor poison'))

    def current_spell(self):
        """
        Currently selected spell

        :returns: currently selected spell
        :rtype: String
        """
        return "fireball"

class AnimatedLabel(QLabel):
    """
    Label to display an animated icon

    .. versionadded:: 0.10
    """
    def __init__(self, timer = None):
        """
        Default constructor
        """
        super().__init__()
        self.tiles = []
        if timer:
            timer.register(self)

    def setPixmap(self, icon):
        """
        Set picture shown in this label
        """
        if hasattr(icon, 'alphaChannel'):
            super().setPixmap(icon)
        else:
            super().setPixmap(icon[0])
            self.tiles = icon

    def animate(self, frame):
        """
        Move animation to given frame

        .. versionadded:: 0.10
        """
        self.setPixmap(self.tiles[frame])

class TimerAdapter():
    """
    Class to trigger animations on glyphs

    .. versionadded:: 0.10
    """
    def __init__(self):
        """
        Default constructor
        """
        self.glyphs = []
        self.frame = 0

    def register(self, glyph):
        """
        Register glyph to internal list
        """
        self.glyphs.append(glyph)

    def trigger_animations(self):
        """
        Process timer event
        """
        self.frame = self.frame + 1
        if self.frame > 1:
            self.frame = 0

        for glyph in self.glyphs:
            glyph.animate(self.frame)

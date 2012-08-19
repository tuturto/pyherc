#!/usr/bin/env python
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
Module displaying events on screen
"""
from PyQt4.QtGui import QTextEdit, QWidget, QHBoxLayout
import PyQt4.QtGui

class EventMessageDisplay(QWidget):
    """
    Widget to display event messages
    """
    def __init__(self, parent):
        """
        Default constructor
        """
        super(EventMessageDisplay, self).__init__(parent)

        self.__set_layout()
        self.__set_events_to_display()

    def __set_layout(self):
        """
        Set layout of this component
        """
        self.horizontal_layout = QHBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText('You set out to adventure')

        self.horizontal_layout.addWidget(self.text_edit)

        self.setLayout(self.horizontal_layout)

    def __set_events_to_display(self):
        """
        Configure events to display
        """
        self.event_types_to_show = ['attack hit',
                                    'attack miss',
                                    'attack nothing',
                                    'poison triggered',
                                    'poison ended',
                                    'poisoned']

    def set_point_of_view(self, character):
        """
        Set point of view for events to display
        """
        self.character = character

    def receive_event(self, event):
        """
        Receive event to display
        """
        if event.event_type in self.event_types_to_show:
            self.text_edit.append(event.get_description(self.character))

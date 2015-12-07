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
Module displaying events on screen
"""
from PyQt4.QtGui import QDockWidget, QHBoxLayout, QTextEdit, QWidget
from pyherc.data import level_name, level_description
from pyherc.events import e_event_type, e_character, e_level

class EventMessageDockWidget(QDockWidget):
    """
    Dock widget to display event messages

    .. versionadded:: 0.5
    """
    def __init__(self, parent, character):
        """
        Default constructor
        """
        super(EventMessageDockWidget, self).__init__(parent)

        self.character = character

        self.__set_layout(character)

    def __set_layout(self, character):
        """
        Set layout of this widget
        """
        self.message_display = EventMessageWidget(self)
        self.setWidget(self.message_display)
        self.setWindowTitle('Messages')

        character.register_event_listener(self.message_display)
        self.message_display.set_point_of_view(character)


class EventMessageWidget(QWidget):
    """
    Widget to display event messages

    .. versionadded:: 0.5
    """
    def __init__(self, parent):
        """
        Default constructor
        """
        super(EventMessageWidget, self).__init__(parent)

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
                                    'poisoned',
                                    'heal started',
                                    'heal ended',
                                    'heal triggered',
                                    'death',
                                    'pick up',
                                    'drop',
                                    'damage triggered',
                                    'equip',
                                    'unequip',
                                    'error',
                                    'mitosis',
                                    'dig',
                                    'new level']

    def set_point_of_view(self, character):
        """
        Set point of view for events to display
        """
        self.character = character

    def receive_event(self, event):
        """
        Receive event to display
        """
        if e_event_type(event) in self.event_types_to_show:
            if e_event_type(event) == 'new level':
                if e_character(event) is self.character:
                    self.text_edit.append("You have reached new level: {0}\n{1}".format(
                        level_name(e_level(event)),
                        level_description(e_level(event))))
            else:
                pass
                # self.text_edit.append(event.get_description(self.character))

# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
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
Module for UI Configuration
"""
from PyQt4.QtCore import Qt


class QtControlsConfiguration():
    """
    Configuration for user interface controls

    .. versionadded:: 0.8
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.move_left = [Qt.Key_4, Qt.Key_Left, Qt.Key_H, Qt.Key_A]
        self.move_up_left = []
        self.move_up = [Qt.Key_8, Qt.Key_Up, Qt.Key_K, Qt.Key_W]
        self.move_up_right = []
        self.move_right = [Qt.Key_6, Qt.Key_Right, Qt.Key_L, Qt.Key_D]
        self.move_down_right = []
        self.move_down = [Qt.Key_2, Qt.Key_Down, Qt.Key_J, Qt.Key_S]
        self.move_down_left = []

        self.action_a = [Qt.Key_Space, Qt.Key_Z, Qt.Key_5]
        self.action_b = [Qt.Key_Control, Qt.Key_X]
        self.action_x = [Qt.Key_Alt]
        self.action_y = [Qt.Key_Tab]

        self.start = [Qt.Key_Return]
        self.back = [Qt.Key_Escape, Qt.Key_C]

        self.left_shoulder = [Qt.Key_Insert, Qt.Key_PageUp, Qt.Key_Q]
        self.right_shoulder = [Qt.Key_Delete, Qt.Key_PageDown]

        self.mode_1 = [Qt.Key_Home]
        self.mode_2 = [Qt.Key_End]

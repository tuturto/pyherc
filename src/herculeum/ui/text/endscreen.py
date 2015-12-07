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
Module for end screen
"""
from datetime import date


class EndScreen():
    """
    Screen for displaying end of the game results

    .. versionadded:: 0.9
    """
    def __init__(self, model, dying_rules, screen,
                 controller):
        """
        Default constructor
        """
        super(EndScreen, self).__init__()

        self.model = model
        self.dying_rules = dying_rules
        self.screen = screen.derwin(18, 40, 5, 20)
        self.controller = controller

    def show(self):
        """
        Display the screen
        """
        self.screen.clear()
        self.screen.border()

        self.screen.addstr(2, 2, 'Date: {0}'.format(date.today()))
        self.screen.addstr(3, 2, 'Score: {0}'.format(
                                        self.dying_rules.calculate_score(
                                                        self.model.player)))
        self.screen.addstr(5, 2, self.controller.get_end_description(
                                                    self.model.end_condition))

        self.screen.refresh()
        self.screen.getch()

#!/usr/bin/env python3
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

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
Module for main window related functionality
"""

from PyQt4.QtGui import QMainWindow, QAction, QIcon, QVBoxLayout, QWorkspace
import PyQt4.QtGui
import os

class MainWindow(QMainWindow):
    """
    Class for displaying main window
    """
    def __init__(self, application, surface_manager):
        """
        Default constructor
        """
        super(MainWindow, self).__init__()

        self.application = application
        self.surface_manager = surface_manager

        self.set_layout()

    def set_layout(self):

        #surface manager?
        exitAction = QAction(QIcon(os.path.join(self.application.base_path,
                                                'wooden-door.png')),
                             '&Quit',
                             self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Quit game')
        exitAction.triggered.connect(PyQt4.QtGui.qApp.quit)

        self.toolbar = self.addToolBar('Quit')
        self.toolbar.addAction(exitAction)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.ws = QWorkspace(self)
        self.ws.setScrollBarsEnabled(True)
        self.setCentralWidget(self.ws)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Herculeum')
        self.show()

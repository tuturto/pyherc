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
Module for help
"""
from PyQt4.QtGui import QDialog, QSplitter, QVBoxLayout, QTextBrowser
from PyQt4.QtHelp import QHelpEngine
from PyQt4.QtCore import Qt, QString, QVariant
import os

class HelpProvider(object):
    """
    Class to provide help files

    .. versionadded:: 0.7
    """
    def __init__(self, base_directory):
        """
        Default constructor
        """
        super(HelpProvider, self).__init__()
        self.help_engine = QHelpEngine('herculeum.qhc');
        self.help_engine.setupData()
        self.help_engine.setCurrentFilter('herculeum')

    def show_help(self, topic):
        """
        Show help for given subject
        """
        dialog = HelpDialog(None, self.help_engine)
        dialog.show_help('test')
        dialog.exec_()

class HelpDialog(QDialog):
    """
    Class to show help

    .. versionadded:: 0.7
    """
    def __init__(self, parent, engine):
        """
        Default constructor
        """
        super(HelpDialog, self).__init__(parent)

        self.help_engine = engine

    def show_help(self, topic):
        contentModel = self.help_engine.contentModel()
        contentWidget = self.help_engine.contentWidget()

        contentWidget.setModel(contentModel)
        contentWidget.clicked.connect(self.open_new_page)

        splitter = QSplitter()
        splitter.addWidget(contentWidget)

        self.help_text = HelpBrowser(self, self.help_engine)
        splitter.addWidget(self.help_text)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(splitter)

        self.setLayout(vertical_layout)

        contentModel.createContents('index')

    def open_new_page(self, index):
        content = self.help_engine.contentModel().contentItemAt(index)

        #data = self.help_engine.fileData(content.url())
        #self.help_text.setHtml(QString(data))
        self.help_text.setSource(content.url())


class HelpBrowser(QTextBrowser):
    """
    Browser for help files

    .. versionadded:: 0.7
    """
    def __init__(self, parent, help_engine):
        """
        Default constructor
        """
        super(HelpBrowser, self).__init__(parent)

        self.help_engine = help_engine

    def loadResource(self, type, url):
        if url.scheme() == 'qthelp':
            return QVariant(self.help_engine.fileData(url))
        else:
            return super(HelpBrowser, self).loadResource(type, url)

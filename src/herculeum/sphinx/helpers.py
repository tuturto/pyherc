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
Module for helpers
"""
from herculeum.config import Configuration
from pyherc.data.model import Model
import herculeum.config.levels
from herculeum.ui.gui import QtControlsConfiguration, QtSurfaceManager
from PyQt4.QtGui import QApplication
import herculeum.ui.gui.resources

qt_app = None
world = None
config = None

def with_config(fn):
    """
    Decorator to inject configuration
    """

    def configured(*args, **kwargs):
        """
        Inject configuration
        """

        if herculeum.sphinx.helpers.config == None:
           herculeum.sphinx.helpers.qt_app = QApplication([])
           herculeum.sphinx.helpers.world = Model()
           herculeum.sphinx.helpers.config = Configuration(
                                                herculeum.sphinx.helpers.world,
                                                herculeum.config.levels,
                                                QtControlsConfiguration(),
                                                QtSurfaceManager())
           herculeum.sphinx.helpers.config.initialise()

        kwargs['config'] = config

        return fn(*args, **kwargs)

    return configured

def shutdown_application(app, env, docname):
    """
    Shutdown qt application
    """
    if herculeum.sphinx.helpers.qt_app != None:
        herculeum.sphinx.helpers.qt_app = None

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
Module for helpers
"""
import herculeum.config.levels
import herculeum.ui.gui.resources
from herculeum.config import Configuration
from herculeum.ui.gui import QtControlsConfiguration, QtSurfaceManager
from pyherc.data.model import Model
from PyQt4.QtGui import QApplication

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

        if herculeum.sphinx.helpers.config is None:
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
    if herculeum.sphinx.helpers.qt_app is not None:
        herculeum.sphinx.helpers.qt_app = None

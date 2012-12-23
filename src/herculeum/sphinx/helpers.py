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
Module for helpers
"""
import os.path
from herculeum.config import Configuration
from pyherc.data.model import Model
import sys
import logging
import herculeum.config.levels
import herculeum.gui.resources
from PyQt4.QtGui import QApplication

qt_app = None
world = None
config = None

def with_config(fn):

    def configured(*args, **kwargs):

        if herculeum.sphinx.helpers.config == None:
           herculeum.sphinx.helpers.qt_app = QApplication([])
           herculeum.sphinx.helpers.world = Model()
           herculeum.sphinx.helpers.config = Configuration('',
                                            herculeum.sphinx.helpers.world,
                                            herculeum.config.levels)
           herculeum.sphinx.helpers.config.initialise()

        kwargs['config'] = config

        return fn(*args, **kwargs)

    return configured

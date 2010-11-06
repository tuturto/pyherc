#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2009 Tuukka Turto
#
#   This file is part of pyMUD.
#
#   pyMUD is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyMUD is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyMUD.  If not, see <http://www.gnu.org/licenses/>.

import pyHerc
from pyHerc.configuration import Configuration

def test_configuration_Creation():
    """
    Just simple test to get configuration created
    """
    config = Configuration()
    assert not (config is None)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Main entry point for Herculeum - game
"""
import sys
import os.path

INSTALL_PATH = os.path.abspath(".")
sys.path.append(INSTALL_PATH)

from herculeum.application import Application

try:
    from herculeum.ui.gui import QtUserInterface, QtControlsConfiguration
    from herculeum.ui.gui import QtSurfaceManager
    import herculeum.ui.gui.resources
except:
    print('Qt user interface is not available')

try:
    from herculeum.ui.text import CursesUserInterface, CursesControlsConfiguration
    from herculeum.ui.text import CursesSurfaceManager
except:
    print('Curses user interface is not available')

if __name__ == "__main__":

    print('#   pyherc is free software: you can redistribute it and/or modify')
    print('#   it under the terms of the GNU General Public License as published by')
    print('#   the Free Software Foundation, either version 3 of the License, or')
    print('#   (at your option) any later version.')
    print('#')
    print('#   pyherc is distributed in the hope that it will be useful,')
    print('#   but WITHOUT ANY WARRANTY; without even the implied warranty of')
    print('#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the')
    print('#   GNU General Public License for more details.')
    print('#')
    print('#   You should have received a copy of the GNU General Public License')
    print('#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.')

    app = Application()
    app.process_command_line()

    if app.ui_mode == 'qt':
        user_interface = QtUserInterface(app)
        surface_manager = QtSurfaceManager()
        controls_configuration = QtControlsConfiguration()
    else:
        user_interface = CursesUserInterface(app)
        surface_manager = CursesSurfaceManager()
        controls_configuration = CursesControlsConfiguration()

    user_interface.show_splash_screen()
    app.start_logging()
    app.load_configuration(controls_configuration,
                           surface_manager)

    app.run(user_interface)


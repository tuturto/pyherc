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
Module for main map related functionality
"""
from PyQt4.QtGui import QMdiSubWindow, QWidget, QHBoxLayout
from PyQt4.QtGui import QGraphicsPixmapItem, QGraphicsView, QGraphicsScene
from PyQt4.QtCore import QSize

class PlayMapWindow(QMdiSubWindow):
    """
    Window for displaying playing world

    .. versionadded:: 0.5
    """
    def __init__(self, parent, model, surface_manager):
        """
        Default constructor
        """
        super(PlayMapWindow, self).__init__(parent)

        self.model = model
        self.surface_manager = surface_manager

        self.__set_layout(model, surface_manager)

    def __set_layout(self, model, surface_manager):
        """
        Set layout of this window
        """
        self.map_widget = PlayMapWidget(parent = self,
                                        model = model,
                                        surface_manager = surface_manager)

        self.setWidget(self.map_widget)

        self.setWindowTitle('Map')

        self.resize(QSize(640, 480))

class PlayMapWidget(QWidget):
    """
    Widget for displaying playing world

    .. versionadded:: 0.5
    """
    def __init__(self, parent, model, surface_manager):
        """
        Default constructor
        """
        super(PlayMapWidget, self).__init__(parent)

        self.model = model
        self.scene = None
        self.surface_manager = surface_manager

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.scene = self.construct_scene(self.model)

        layout = QHBoxLayout()

        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.setLayout(layout)


    def construct_scene(self, model):
        """
        Constructs scene to display
        """
        new_scene = QGraphicsScene()

        level = model.player.level
        size = level.get_size()

        for loc_x in range(0, size[0]):
            for loc_y in range(0, size[1]):
                new_glyph = MapGlyph(self.surface_manager.get_icon(level.get_tile(loc_x, loc_y)))
                new_glyph.setPos(loc_x * 32, loc_y * 32)
                new_scene.addItem(new_glyph)

        return new_scene

class MapGlyph(QGraphicsPixmapItem):
    """
    Widget to represent a glyph on map
    """
    def __init__(self, pixmap):
        """
        Default constructor
        """
        super(MapGlyph, self).__init__(pixmap, None)

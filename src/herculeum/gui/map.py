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
from PyQt4.QtCore import QSize, Qt

class PlayMapWindow(QMdiSubWindow):
    """
    Window for displaying playing world

    .. versionadded:: 0.5
    """
    def __init__(self, parent, model, surface_manager, action_factory, rng):
        """
        Default constructor
        """
        super(PlayMapWindow, self).__init__(parent)

        self.model = model
        self.surface_manager = surface_manager
        self.action_factory = action_factory
        self.rng = rng

        self.__set_layout(model, surface_manager, action_factory, rng)

    def __set_layout(self, model, surface_manager, action_factory, rng):
        """
        Set layout of this window
        """
        self.map_widget = PlayMapWidget(parent = self,
                                        model = model,
                                        surface_manager = surface_manager,
                                        action_factory = action_factory,
                                        rng = rng)

        self.setWidget(self.map_widget)

        self.setWindowTitle('Map')

        self.resize(QSize(640, 480))

class PlayMapWidget(QWidget):
    """
    Widget for displaying playing world

    .. versionadded:: 0.5
    """
    def __init__(self, parent, model, surface_manager, action_factory, rng):
        """
        Default constructor
        """
        super(PlayMapWidget, self).__init__(parent)

        self.model = model
        self.scene = None
        self.surface_manager = surface_manager
        self.action_factory = action_factory
        self.rng = rng

        self.move_key_map = {Qt.Key_8:1, Qt.Key_9:2, Qt.Key_6:3, Qt.Key_3:4,
                             Qt.Key_2:5, Qt.Key_1:6, Qt.Key_4:7, Qt.Key_7:8,
                             Qt.Key_5:9}

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.scene = self.__construct_scene(self.model)

        layout = QHBoxLayout()

        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.setLayout(layout)


    def __construct_scene(self, model):
        """
        Constructs scene to display
        """
        new_scene = QGraphicsScene()

        level = model.player.level
        size = level.get_size()

        for loc_x in range(0, size[0]):
            for loc_y in range(0, size[1]):
                new_glyph = MapGlyph(self.surface_manager.get_icon(level.get_tile(loc_x, loc_y)),
                                     None)
                new_glyph.setPos(loc_x * 32, loc_y * 32)
                new_scene.addItem(new_glyph)

        for portal in level.portals:
                new_glyph = MapGlyph(self.surface_manager.get_icon(portal.icon),
                                     portal)
                new_glyph.setPos(portal.location[0] * 32, portal.location[1] * 32)
                new_scene.addItem(new_glyph)

        for item in level.items:
                new_glyph = MapGlyph(self.surface_manager.get_icon(item.icon),
                                     item)
                new_glyph.setPos(item.location[0] * 32, item.location[1] * 32)
                new_scene.addItem(new_glyph)

        for creature in level.creatures:
                new_glyph = MapGlyph(self.surface_manager.get_icon(creature.icon),
                                     creature)
                new_glyph.setPos(creature.location[0] * 32, creature.location[1] * 32)
                new_scene.addItem(new_glyph)

        return new_scene

    def keyPressEvent(self, event):
        """
        Handle key events
        """
        key_code = event.key()

        player = self.model.player
        next_creature = self.model.get_next_creature()

        if next_creature == player:

            if key_code in self.move_key_map.keys():
                direction = self.move_key_map[key_code]

                if player.is_move_legal(direction,
                                        'walk',
                                        self.action_factory):
                    player.move(direction,
                                self.action_factory)
                elif direction != 9:
                    player.perform_attack(direction,
                                          self.action_factory,
                                          self.application.rng)
        else:
            while next_creature != player:
                next_creature.act(model = self.model,
                                  action_factory = self.action_factory,
                                  rng = self.rng)
                next_creature = self.model.get_next_creature()


class MapGlyph(QGraphicsPixmapItem):
    """
    Widget to represent a glyph on map
    """
    def __init__(self, pixmap, entity):
        """
        Default constructor
        """
        super(MapGlyph, self).__init__(pixmap, None)

        self.entity = entity

        if entity != None:
            entity.register_for_updates(self)

    def receive_update(self, entity):
        """
        Receive event from model
        """
        if entity.location != None:
            self.setPos(self.entity.location[0] * 32,
                        self.entity.location[1] * 32)

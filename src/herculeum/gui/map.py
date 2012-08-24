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
        self.current_level = None

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
        self.scene = QGraphicsScene()
        self.__construct_scene(self.model, self.scene)

        layout = QHBoxLayout()

        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.model.player.register_for_updates(self)
        self.model.register_event_listener(self)
        self.__center_view_on_character(self.model.player)

        self.setLayout(layout)

    def __center_view_on_character(self, entity):
        """
        Center view on given entity
        """
        location = entity.location
        width = 320
        height = 320

        self.view.setSceneRect((location[0] * 32) - width // 2,
                              (location[1] * 32) - height // 2,
                              width,
                              height)

    def __construct_scene(self, model, scene):
        """
        Constructs scene to display
        """
        for item in scene.items():
            item.clear_update_registration()

        scene.clear()

        self.current_level = model.player.level
        size = self.current_level.get_size()

        for loc_x in range(0, size[0]):
            for loc_y in range(0, size[1]):
                new_glyph = MapGlyph(self.surface_manager.get_icon(self.current_level.get_tile(loc_x, loc_y)),
                                     None)
                new_glyph.setZValue(0)
                new_glyph.setPos(loc_x * 32, loc_y * 32)
                scene.addItem(new_glyph)

        for portal in self.current_level.portals:
                self.add_glyph(portal, scene, 1)

        for item in self.current_level.items:
                self.add_glyph(item, scene, 2)

        for creature in self.current_level.creatures:
                self.add_glyph(creature, scene, 3)

    def add_glyph(self, entity, scene, z_order):
        """
        Add graphical representation of an entity

        :param entity: entity to display
        :param scene: scene where glyph will be added
        :type scene: QGraphicsScene
        :param z_order: z-order of entity being displayed
        :type z_order: int
        """
        new_glyph = MapGlyph(self.surface_manager.get_icon(entity.icon),
                             entity)
        new_glyph.setZValue(z_order)
        new_glyph.setPos(entity.location[0] * 32,
                         entity.location[1] * 32)
        scene.addItem(new_glyph)

    def receive_event(self, event):
        """
        Receive event from model
        """
        if event.event_type == 'death':
            glyphs = [x for x in self.view.items()
                      if x.entity == event.deceased]

            for glyph in glyphs:
                self.view.scene().removeItem(glyph)
        elif event.event_type == 'pick up':
            glyphs = [x for x in self.view.items()
                      if x.entity == event.item]

            for glyph in glyphs:
                self.view.scene().removeItem(glyph)

        elif event.event_type == 'drop':
            self.add_glyph(event.item, self.scene, 2)

    def receive_update(self, event):
        """
        Receive update from entity
        """
        if event.event_type == 'move':
            if self.model.player.level != self.current_level:
                self.__construct_scene(self.model, self.scene)
            self.__center_view_on_character(self.model.player)


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
                                          self.rng)

        next_creature = self.model.get_next_creature()
        while next_creature != player:
            next_creature.act(model = self.model,
                              action_factory = self.action_factory,
                              rng = self.rng)
            next_creature = self.model.get_next_creature()


class MapGlyph(QGraphicsPixmapItem):
    """
    Widget to represent a glyph on map

    .. versionadded:: 0.5
    """
    def __init__(self, pixmap, entity):
        """
        Default constructor
        """
        super(MapGlyph, self).__init__(pixmap, None)

        self.entity = entity

        if entity != None:
            entity.register_for_updates(self)

    def receive_update(self, event):
        """
        Receive event from model
        """
        if event.event_type == 'move':
            location = event.mover.location
            if location != None:
                self.setPos(location[0] * 32,
                            location[1] * 32)

    def clear_update_registration(self):
        """
        Clear update registrations
        """
        if self.entity != None:
            self.entity.remove_from_updates(self)

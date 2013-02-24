#!/usr/bin/env python
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
Module for main map related functionality
"""
try:
    from PyQt4.QtGui import QMdiSubWindow, QWidget, QHBoxLayout, QVBoxLayout
    from PyQt4.QtGui import QGraphicsPixmapItem, QGraphicsView, QGraphicsScene
    from PyQt4.QtGui import QGraphicsSimpleTextItem, QColor
    from PyQt4.QtGui import QFont
    from PyQt4.QtCore import QSize, Qt, QPropertyAnimation, QObject, pyqtProperty
    from PyQt4.QtCore import QAbstractAnimation, QSequentialAnimationGroup
    from PyQt4.QtCore import QEasingCurve, pyqtSignal, QEvent
except:
    pass

from herculeum.ui.gui.eventdisplay import EventMessageWidget
from herculeum.ui.gui.widgets import HitPointsWidget, EffectsWidget
from herculeum.ui.controllers import MoveController
from random import Random

class PlayMapWindow(QWidget):
    """
    Window for displaying playing world

    .. versionadded:: 0.5
    """
    def __init__(self, parent, model, surface_manager, action_factory, rng,
                 rules_engine, configuration):
        """
        Default constructor
        """
        super(PlayMapWindow, self).__init__(parent)

        self.model = model
        self.surface_manager = surface_manager
        self.action_factory = action_factory
        self.rng = rng
        self.current_level = None
        self.configuration = configuration

        self.__set_layout(model, surface_manager, action_factory, rng,
                          rules_engine, configuration)

    MenuRequested = pyqtSignal(name='MenuRequested')
    EndScreenRequested = pyqtSignal(name='EndScreenRequested')

    def __set_layout(self, model, surface_manager, action_factory, rng,
                     rules_engine, configuration):
        """
        Set layout of this window
        """
        layout = QVBoxLayout()
        status_layout = QHBoxLayout()

        self.hit_points_widget = HitPointsWidget(parent = self)
        self.effects_widget = EffectsWidget(parent = self,
                                            surface_manager = surface_manager)

        self.map_widget = PlayMapWidget(parent = self,
                                        model = model,
                                        surface_manager = surface_manager,
                                        action_factory = action_factory,
                                        rng = rng,
                                        rules_engine = rules_engine,
                                        configuration = configuration)
        self.map_widget.MenuRequested.connect(self.on_menu_requested)
        self.map_widget.EndScreenRequested.connect(self.on_end_screen_requested)

        self.message_widget = EventMessageWidget(parent = self)
        self.message_widget.setMaximumHeight(100)

        status_layout.addWidget(self.hit_points_widget)
        status_layout.addWidget(self.effects_widget)
        status_layout.addStretch()

        layout.addLayout(status_layout)
        layout.addWidget(self.map_widget)
        layout.addWidget(self.message_widget)
        self.setLayout(layout)
        self.resize(QSize(640, 480))

    def construct_scene(self):
        """
        Create scene to display
        """
        self.map_widget.construct_scene()
        self.model.player.register_event_listener(self.message_widget)
        self.message_widget.set_point_of_view(self.model.player)
        self.model.player.register_for_updates(self.effects_widget)

    def on_menu_requested(self):
        """
        Handle requesting menu window
        """
        self.MenuRequested.emit()

    def on_end_screen_requested(self):
        """
        Handle requesting end screen

        .. versionadded:: 0.8
        """
        self.EndScreenRequested.emit()

class PlayMapWidget(QWidget):
    """
    Widget for displaying playing world

    .. versionadded:: 0.5
    """
    def __init__(self, parent, model, surface_manager, action_factory, rng,
                 rules_engine, configuration):
        """
        Default constructor
        """
        super(PlayMapWidget, self).__init__(parent)

        self.model = model
        self.scene = None
        self.surface_manager = surface_manager
        self.action_factory = action_factory
        self.rng = rng
        self.rules_engine = rules_engine
        self.configuration = configuration

        self.animations = []
        self.move_controller = MoveController(action_factory = action_factory,
                                              rng = rng)

        self.__set_layout()
        self.keymap, self.move_key_map = self._construct_keymaps(
                                                        configuration.controls)

    MenuRequested = pyqtSignal(name='MenuRequested')
    EndScreenRequested = pyqtSignal(name='EndScreenRequested')

    def _construct_keymaps(self, config):
        """
        Construct keymaps for handling input
        """
        keymap = {}
        move_keymap = {}
        for key in config.move_left:
            keymap[key] = self._move
            move_keymap[key] = 7
        for key in config.move_up_left:
            keymap[key] = self._move
            move_keymap[key] = 8
        for key in config.move_up:
            keymap[key] = self._move
            move_keymap[key] = 1
        for key in config.move_up_right:
            keymap[key] = self._move
            move_keymap[key] = 2
        for key in config.move_right:
            keymap[key] = self._move
            move_keymap[key] = 3
        for key in config.move_down_right:
            keymap[key] = self._move
            move_keymap[key] = 4
        for key in config.move_down:
            keymap[key] = self._move
            move_keymap[key] = 5
        for key in config.move_down_left:
            keymap[key] = self._move
            move_keymap[key] = 6
        for key in config.start:
            keymap[key] = self._menu
        for key in config.action_a:
            keymap[key] = self._action_a

        return keymap, move_keymap

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.scene = QGraphicsScene()

        layout = QHBoxLayout()

        self.view = QGraphicsView(self.scene)
        self.view.setFocusPolicy(Qt.StrongFocus)
        self.view.installEventFilter(self)
        layout.addWidget(self.view)

        self.setLayout(layout)

    def construct_scene(self):
        """
        Construct scene to display
        """
        self.__construct_scene(self.model, self.scene)

        self.model.player.register_for_updates(self)
        self.model.register_event_listener(self)
        self.__center_view_on_character(self.model.player)

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
        for item in (item for item in scene.items()
                     if hasattr(item, 'clear_update_registration')):
            item.clear_update_registration()

        for anim in [x for x in self.animations]:
            anim.clear()

        self.animations = []

        scene.clear()

        self.current_level = model.player.level
        size = self.current_level.get_size()

        for loc_x, column in enumerate(self.current_level.floor):
            for loc_y, tile in enumerate(column):
                new_glyph = MapGlyph(self.surface_manager.get_icon(tile),
                                     None)
                new_glyph.setZValue(0)
                new_glyph.setPos(loc_x * 32, loc_y * 32)
                scene.addItem(new_glyph)

        for loc_x, column in enumerate(self.current_level.walls):
            for loc_y, tile in enumerate(column):
                new_glyph = MapGlyph(self.surface_manager.get_icon(tile),
                                     None)
                new_glyph.setZValue(1)
                new_glyph.setPos(loc_x * 32, loc_y * 32)
                scene.addItem(new_glyph)

        for portal in self.current_level.portals:
                self.add_glyph(portal, scene, 10)

        for item in self.current_level.items:
                self.add_glyph(item, scene, 20)

        for creature in self.current_level.creatures:
                self.add_glyph(creature, scene, 30)

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
                      if (hasattr(x, 'entity'))
                      and (x.entity == event.deceased)]

            for glyph in glyphs:
                self.view.scene().removeItem(glyph)

            if event.deceased == self.model.player:
                self.EndScreenRequested.emit()
        elif event.event_type == 'pick up':
            glyphs = [x for x in self.view.items()
                      if (hasattr(x, 'entity'))
                      and (x.entity == event.item)]

            for glyph in glyphs:
                self.view.scene().removeItem(glyph)

        elif event.event_type == 'drop':
            self.add_glyph(event.item, self.scene, 20)
        elif event.event_type == 'attack hit':
            damage = event.damage.damage_inflicted
            self.show_damage_counter(event.target.location,
                                     -damage,
                                     'white')
        elif event.event_type == 'damage triggered':
            damage = event.damage
            self.show_damage_counter(event.target.location,
                                     -damage,
                                     'red',
                                     (0, 16))
        elif event.event_type == 'poisoned':
            self.show_status_counter(event.target.location,
                                     'poisoned',
                                     'green',
                                     (0, 16))
        elif event.event_type == 'poison triggered':
            self.show_damage_counter(event.target.location,
                                     -event.damage,
                                     'green',
                                     (0, 16))
        elif event.event_type == 'heal started':
            self.show_status_counter(event.target.location,
                                     'healing',
                                     'blue',
                                     (0, 16))
        elif event.event_type == 'heal triggered':
            self.show_damage_counter(event.target.location,
                                     event.healing,
                                     'blue',
                                     (0, 16));
        elif event.event_type == 'notice':
            self.show_status_counter(event.character.location,
                                     '!',
                                     'red',
                                     (0, 16))
        elif event.event_type == 'lose focus':
            self.show_status_counter(event.character.location,
                                     '?',
                                     'yellow',
                                     (0, 16))

    def show_status_counter(self, location, status, colour, offset = (0, 0)):
        """
        Show status counter
        """
        damage_counter = DamageCounter(damage = str(status),
                                       colour = colour,
                                       parent = self)
        self.view.scene().addItem(damage_counter)

        bounds = damage_counter.boundingRect()
        width = bounds.width()

        damage_counter.setPos(location[0] * 32 + 16 - (width / 2) + offset[0],
                              location[1] * 32 + offset[1])

        animation = QSequentialAnimationGroup()

        moving = QPropertyAnimation(damage_counter.adapter,
                                    'y_location')
        moving.setDuration(750)
        moving.setStartValue(location[1] * 32)
        moving.setEndValue(location[1] * 32 - 32)

        animation.addAnimation(moving)

        fading = QPropertyAnimation(damage_counter.adapter,
                                    'opacity')
        fading.setDuration(750)
        fading.setStartValue(1.0)
        fading.setEndValue(0.0)
        animation.addAnimation(fading)

        animation.finished.connect(self.remove_finished_animation)
        self.animations.append(animation)

        animation.start()

    def show_damage_counter(self, location, damage, colour, offset = (0, 0)):
        """
        Show damage counter
        """
        damage_counter = DamageCounter(damage = str(damage),
                                       colour = colour,
                                       parent = self)
        self.view.scene().addItem(damage_counter)

        bounds = damage_counter.boundingRect()
        width = bounds.width()

        rand = Random()

        damage_counter.setPos((location[0] * 32
                                    + 16 - (width / 2)
                                    + rand.randint(-16, 16))
                                    + offset[0],
                              location[1] * 32 + offset[1])

        animation = QSequentialAnimationGroup()

        moving = QPropertyAnimation(damage_counter.adapter,
                                    'y_location')
        moving.setDuration(750)
        moving.setStartValue(location[1] * 32 + offset[1])
        moving.setEndValue(location[1] * 32 - 32 + offset[1])
        curve = QEasingCurve(QEasingCurve.OutElastic)
        moving.setEasingCurve(curve)
        animation.addAnimation(moving)

        fading = QPropertyAnimation(damage_counter.adapter,
                                    'opacity')
        fading.setDuration(750)
        fading.setStartValue(1.0)
        fading.setEndValue(0.0)
        animation.addAnimation(fading)

        animation.finished.connect(self.remove_finished_animation)
        self.animations.append(animation)

        animation.start()

    def remove_finished_animation(self):
        """
        Remove finished animation
        """
        finished_animations  = (x for x in self.animations
                                if x.state() == QAbstractAnimation.Stopped)
        counters = (x.animationAt(0).targetObject().object_to_animate
                    for x in finished_animations)

        for item in finished_animations:
            item.clear()
            self.animations.remove(item)

        for item in counters:
            self.view.scene().removeItem(item)

    def receive_update(self, event):
        """
        Receive update from entity
        """
        if event.event_type == 'move':
            if self.model.player.level != self.current_level:
                self.__construct_scene(self.model, self.scene)
            self.__center_view_on_character(self.model.player)

    def eventFilter(self, qobject, event):
        """
        Filter events

        .. Note:: This is done in order to process cursor keys
        """
        result = False

        if event.type() == QEvent.KeyPress:
            self.keyPressEvent(event)
            result = True
        else:
            result = super(PlayMapWidget, self).eventFilter(qobject, event)

        return result

    def keyPressEvent(self, event):
        """
        Handle key events
        """
        if self.model.player is None:
            return

        key_code = event.key()

        player = self.model.player
        next_creature = self.model.get_next_creature(self.rules_engine)

        if next_creature == player:

            if key_code in self.keymap:
                self.keymap[key_code](key_code, event.modifiers())

        next_creature = self.model.get_next_creature(self.rules_engine)
        while next_creature != player and next_creature != None:
            next_creature.act(model = self.model,
                              action_factory = self.action_factory,
                              rng = self.rng)
            next_creature = self.model.get_next_creature(self.rules_engine)

        if self.model.end_condition != 0:
            self.EndScreenRequested.emit()

    def _move(self, key, modifiers):
        """
        Process movement key

        :param key: key triggering the processing
        :type key: int
        """
        player = self.model.player
        level = player.level
        direction = self.move_key_map[key]

        if modifiers & Qt.ControlModifier:
            if direction != 9:
                player.perform_attack(direction,
                                      self.action_factory,
                                      self.rng)
        else:
            self.move_controller.move_or_attack(player,
                                                direction,
                                                'walk')

    def _menu(self, key, modifiers):
        """
        Process menu key

        :param key: key triggering the processing
        :type key: int
        """
        self.MenuRequested.emit()

    def _action_a(self, key, modifiers):
        """
        Process action a key

        :param key: key triggering the processing
        :type key: int
        """
        player = self.model.player
        level = player.level
        items = level.get_items_at(player.location)

        if items != None and len(items) > 0:
            player.pick_up(items[0],
                           self.action_factory)

        elif player.is_move_legal(9,
                                  'walk',
                                  self.action_factory):
            player.move(9,
                        self.action_factory)

class DamageCounter(QGraphicsSimpleTextItem):
    """
    Counter for showing damage

    .. versionadded:: 0.6
    """
    def __init__(self, damage, colour, parent):
        """
        Default constructor
        """
        super(DamageCounter, self).__init__()

        font = QFont('Helvetica',
                     12,
                     QFont.Bold,
                     False)

        self.setText(str(damage))
        self.setBrush(QColor(colour))
        self.setFont(font)

        self.adapter = DamageCounterAdapter(self, self)

class DamageCounterAdapter(QObject):
    """
    Adapter for damage counter

    .. versionadded:: 0.6
    """
    def __init__(self, parent, object_to_animate):
        """
        Default constructor
        """
        super(DamageCounterAdapter, self).__init__()
        self.object_to_animate = object_to_animate

    def __get_y_location(self):
        return self.object_to_animate.y()

    def __set_y_location(self, y):
        self.object_to_animate.setY(y)

    def __get_opacity(self):
        return self.object_to_animate.opacity()

    def __set_opacity(self, opacity):
        self.object_to_animate.setOpacity(opacity)

    y_location = pyqtProperty(int, __get_y_location, __set_y_location)
    opacity = pyqtProperty(float, __get_opacity, __set_opacity)


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

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
Module for main map related functionality
"""
from random import Random

from herculeum.ui.controllers import MoveController
from herculeum.ui.gui.animations import AnimationFactory
from herculeum.ui.gui.eventdisplay import EventMessageWidget
from herculeum.ui.gui.widgets import (EffectsWidget, HitPointsWidget,
                                      SpellSelectorWidget, TimerAdapter)
from pyherc.data.model import DIED_IN_DUNGEON
from pyherc.rules import attack, cast, is_move_legal, move, pick_up, wait
from PyQt4.QtCore import (pyqtProperty, pyqtSignal, QAbstractAnimation,
                          QEasingCurve, QEvent, QObject, QPropertyAnimation,
                          QSequentialAnimationGroup, QSize, Qt, QTimer)
from PyQt4.QtGui import (QColor, QFont, QGraphicsPixmapItem, QGraphicsScene,
                         QGraphicsSimpleTextItem, QGraphicsView, QHBoxLayout,
                         QTransform, QVBoxLayout, QWidget)
from pyherc.data import get_characters, get_items, get_tiles


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
        super().__init__(parent)

        self.model = model
        self.surface_manager = surface_manager
        self.action_factory = action_factory
        self.rng = rng
        self.current_level = None
        self.configuration = configuration

        self.hit_points_widget = None
        self.message_widget = None
        self.map_widget = None
        self.effects_widget = None
        self.spell_selector = None

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

        self.spell_selector = SpellSelectorWidget(parent = self,
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
        self.map_widget.NextSpellRequested.connect(self.on_next_spell)
        self.map_widget.PreviousSpellRequested.connect(self.on_previous_spell)

        self.message_widget = EventMessageWidget(parent = self)
        self.message_widget.setMaximumHeight(100)

        status_layout.addWidget(self.hit_points_widget)
        status_layout.addWidget(self.spell_selector)
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

    def on_next_spell(self):
        """
        Handle selecting next spell

        .. versionadded:: 0.10
        """
        self.spell_selector.next_spell()

    def on_previous_spell(self):
        """
        Handle selecting previous spell

        .. versionadded:: 0.10
        """
        self.spell_selector.previous_spell()

zorder_floor = 0
zorder_item = 2
zorder_character = 5
zorder_wall = 10
zorder_ornament = 20

zorder_counter = 30

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
        super().__init__(parent)

        self.model = model
        self.scene = None
        self.surface_manager = surface_manager
        self.action_factory = action_factory
        self.rng = rng
        self.rules_engine = rules_engine
        self.configuration = configuration

        self.current_level = None
        self.view = None
        self.animation_adapters = []
        self.animation_timers = []

        for adapter in range(10):
            self.animation_adapters.append(TimerAdapter())
            self.animation_timers.append(QTimer(self))
            self.animation_timers[adapter].timeout.connect(self.animation_adapters[adapter].trigger_animations)
            self.animation_timers[adapter].start(450 + adapter * 10)

        self.animations = []
        self.move_controller = MoveController(action_factory = action_factory,
                                              rng = rng)

        self.__set_layout()
        self.keymap, self.move_key_map = self._construct_keymaps(
                                                        configuration.controls)

        self.animation_factory = AnimationFactory()

    MenuRequested = pyqtSignal(name='MenuRequested')
    EndScreenRequested = pyqtSignal(name='EndScreenRequested')
    NextSpellRequested = pyqtSignal(name='NextSpellRequested')
    PreviousSpellRequested = pyqtSignal(name='PreviousSpellRequested')


    def _construct_keymaps(self, config):
        """
        Construct keymaps for handling input
        """
        keymap = {}
        move_keymap = {}
        for key in config.move_left:
            keymap[key] = self._move
            move_keymap[key] = 7
        for key in config.move_up:
            keymap[key] = self._move
            move_keymap[key] = 1
        for key in config.move_right:
            keymap[key] = self._move
            move_keymap[key] = 3
        for key in config.move_down:
            keymap[key] = self._move
            move_keymap[key] = 5
        for key in config.start:
            keymap[key] = self._menu
        for key in config.action_a:
            keymap[key] = self._action_a
        for key in config.back:
            keymap[key] = self._back
        for key in config.left_shoulder:
            keymap[key] = self._shoulder_left
        for key in config.right_shoulder:
            keymap[key] = self._shoulder_right

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

        for adapter in self.animation_adapters:
            adapter.glyphs.clear()

        for anim in [x for x in self.animations]:
            anim.clear()

        self.animations = []

        scene.clear()

        self.current_level = model.player.level

        for location, tile in get_tiles(self.current_level):
            if tile['\ufdd0:floor']:
                new_glyph = MapGlyph(self.surface_manager.get_icon(tile['\ufdd0:floor']),
                                     None)
                new_glyph.setZValue(zorder_floor)
                new_glyph.setPos(location[0] * 32, location[1] * 32)
                scene.addItem(new_glyph)
            if tile['\ufdd0:wall']:
                new_glyph = MapGlyph(self.surface_manager.get_icon(tile['\ufdd0:wall']),
                                     None)
                new_glyph.setZValue(zorder_wall)
                new_glyph.setPos(location[0] * 32, location[1] * 32)
                scene.addItem(new_glyph)
            if tile['\ufdd0:ornamentation']:
                new_glyph = MapGlyph(self.surface_manager.get_icon(tile['\ufdd0:ornamentation']),
                                     None,
                                     self.rng.choice(self.animation_adapters))
                new_glyph.setZValue(zorder_ornament)
                new_glyph.setPos(location[0] * 32, location[1] * 32)
                scene.addItem(new_glyph)
            for item in tile['\ufdd0:items']:
                self.add_glyph(item, scene, zorder_item)

        for creature in get_characters(self.current_level):
            self.add_glyph(creature,
                           scene,
                           zorder_character)

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
                             entity, self.rng.choice(self.animation_adapters))
        new_glyph.setZValue(z_order)
        new_glyph.setPos(entity.location[0] * 32,
                         entity.location[1] * 32)
        scene.addItem(new_glyph)

    def remove_glyph(self, entity):
        """
        Remove graphical representation of an entity
        """
        glyphs = [x for x in self.view.items()
                  if (hasattr(x, 'entity'))
                  and (x.entity == entity)]

        for glyph in glyphs:
            self.view.scene().removeItem(glyph)

    def receive_event(self, event):
        """
        Receive event from model
        """

        anim = self.animation_factory.create_animation(event)
        anim.trigger(self)

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

    def eventFilter(self, qobject, event): #pylint: disable-msg=C0103
        """
        Filter events

        .. Note:: This is done in order to process cursor keys
        """
        result = False

        if event.type() == QEvent.KeyPress:
            self.keyPressEvent(event)
            result = True
        else:
            result = super().eventFilter(qobject, event)

        return result

    def keyPressEvent(self, event): #pylint: disable-msg=C0103
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

        if next_creature is None:
            self.model.end_condition = DIED_IN_DUNGEON

        while (next_creature != player
                and next_creature != None
                and self.model.end_condition == 0):
            next_creature.act(model = self.model,
                              action_factory = self.action_factory,
                              rng = self.rng)
            next_creature = self.model.get_next_creature(self.rules_engine)

            if next_creature is None:
                self.model.end_condition = DIED_IN_DUNGEON

        if self.model.end_condition != 0:
            self.EndScreenRequested.emit()

    def _move(self, key, modifiers):
        """
        Process movement key

        :param key: key triggering the processing
        :type key: int
        """
        player = self.model.player
        direction = self.move_key_map[key]

        if modifiers & Qt.ControlModifier:
            if direction != 9:
                attack(player,
                       direction,
                       self.action_factory,
                       self.rng)
        elif modifiers & Qt.AltModifier:
            if direction != 9:
                cast(player,
                     direction,
                     'fireball',
                     self.action_factory)

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

    def _back(self, key, modifiers):
        """
        Process back key

        :param key: key triggering the processing
        :type key: int
        """
        wait(self.model.player,
             self.action_factory)

    def _shoulder_right(self, key, modifiers):
        """
        Process right shoulder button

        :param key: key triggering the processing
        :type key: int

        .. versionadded:: 0.10
        """
        self.NextSpellRequested.emit()

    def _shoulder_left(self, key, modifiers):
        """
        Process left shoulder button

        :param key: key triggering the processing
        :type key: int

        .. versionadded:: 0.10
        """
        self.PreviousSpellRequested.emit()

    def _action_a(self, key, modifiers):
        """
        Process action a key

        :param key: key triggering the processing
        :type key: int
        """
        player = self.model.player
        level = player.level
        items = get_items(level, player.location)

        if items != None and len(items) > 0:
            pick_up(player,
                    items[0],
                    self.action_factory)

        elif is_move_legal(player, 9, 'walk', self.action_factory):
            move(player, 9, self.action_factory)

class DamageCounter(QGraphicsSimpleTextItem):
    """
    Counter for showing damage

    .. versionadded:: 0.6
    """
    def __init__(self, damage, colour, parent):
        """
        Default constructor
        """
        super().__init__()

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
        super().__init__()
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
    def __init__(self, pixmap, entity, timer = None):
        """
        Default constructor
        """
        self.tiles = []

        if hasattr(pixmap, 'alphaChannel'):
            super().__init__(pixmap, None)
        else:
            super().__init__(pixmap[0], None)
            if timer:
                timer.register(self)
            self.tiles = pixmap

        self.entity = entity

        self.flipped = False
        self.offset = 0

    def animate(self, frame):
        """
        Move animation to given frame

        .. versionadded:: 0.10
        """
        self.setPixmap(self.tiles[frame])

    def receive_update(self, event):
        """
        Receive event from model
        """
        if event.event_type == 'move':
            location = event.mover.location
            direction = event.direction

            if direction in (2, 3, 4):
                self.flipped = True
                self.offset = 32

            if direction in (6, 7, 8):
                self.flipped = False
                self.offset = 0

            if location != None:
                self.setPos(location[0] * 32 + self.offset,
                            location[1] * 32)

            if self.flipped:
                self.setTransform(QTransform.fromScale(-1, 1))
            else:
                self.setTransform(QTransform.fromScale(1, 1))

    def clear_update_registration(self):
        """
        Clear update registrations
        """
        if self.entity != None:
            self.entity.remove_from_updates(self)

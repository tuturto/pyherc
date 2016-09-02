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
Module for map screen
"""
from herculeum.ui.controllers import EndScreenController, MoveController
from herculeum.ui.text.character import CharacterScreen
from herculeum.ui.text.endscreen import EndScreen
from herculeum.ui.text.inventory import InventoryScreen
from pyherc.aspects import log_debug, log_info
from pyherc.data.model import DIED_IN_DUNGEON
from pyherc.ports import wait, pick_up
from pyherc.events import e_event_type
import pyherc


class MapScreen():
    """
    Class for map screen

    .. versionadded:: 0.9
    """
    @log_debug
    def __init__(self, model, surface_manager, action_factory, rng,
                 rules_engine, configuration, screen):
        """
        Default constructor
        """
        super(MapScreen, self).__init__()

        self.model = model
        self.surface_manager = surface_manager
        self.action_factory = action_factory
        self.rng = rng
        self.rules_engine = rules_engine
        self.configuration = configuration
        self.screen = screen
        self.keymap, self.move_key_map = self._construct_keymaps(
                                                        configuration.controls)
        self.move_controller = MoveController(action_factory,
                                              rng)
        self.messages = []

    @log_debug
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
        for key in config.action_a:
            keymap[key] = self._action_a
        for key in config.back:
            keymap[key] = self._back

        return keymap, move_keymap


    @log_info
    def show(self):
        """
        Show the map
        """
        self.refresh_screen()
        player = self.model.player

        while self.model.end_condition == 0 and player.level is not None:
            next_creature = self.model.get_next_creature(self.rules_engine)

            if next_creature == player:
                self._handle_player_input()
            elif next_creature is not None:
                next_creature.act()
            else:
                self.model.end_condition = DIED_IN_DUNGEON

            self.refresh_screen()

        dialog = EndScreen(model = self.model,
                           dying_rules = self.rules_engine.dying_rules,
                           screen = self.screen,
                           controller = EndScreenController())
        dialog.show()

    @log_debug
    def _handle_player_input(self):
        """
        Handle input from player
        """
        key = chr(self.screen.getch())

        if key in self.keymap:
            self.keymap[key](key)
        elif key == 'i':
            inv = InventoryScreen(character = self.model.player,
                                  config = self.configuration,
                                  screen = self.screen,
                                  action_factory = self.action_factory,
                                  parent = self.screen)
            inv.show()
        elif key == 'c':
            dialog = CharacterScreen(character = self.model.player,
                                     screen = self.screen)
            dialog.show()
        elif key == 'a':
            dir_key = chr(self.screen.getch())
            if dir_key in self.move_key_map:
                direction = self.move_key_map[dir_key]
                pyherc.vtable['\ufdd0:attack'](self.model.player,
                                               direction)
        elif key == 'Q':
            self.model.end_condition = 1

    @log_debug
    def _move(self, key):
        """
        Process movement key

        :param key: key triggering the processing
        :type key: string
        """
        direction = self.move_key_map[key]
        self.move_controller.move_or_attack(self.model.player, direction)

    @log_debug
    def _back(self, key):
        """
        Process back key

        :param key: key triggering the processing
        :type key: int

        .. versionadded:: 0.10
        """
        wait(self.model.player)

    @log_debug
    def _action_a(self, key):
        """
        Process action a key

        :param key: key triggering the processing
        :type key: int
        """
        player = self.model.player
        level = player.level
        items = level.get_items_at(player.location)

        if items is not None and len(items) > 0:
            pick_up(player,
                    items[0])

        elif pyherc.vtable['\ufdd0:is_move_legal'](player, 9, 'walk', self.action_factory):
            pyherc.vtable['\ufdd0:move'](player, 9, self.action_factory)

    @log_debug
    def refresh_screen(self):
        """
        Draw whole screen
        """
        player = self.model.player
        level = player.level

        if level is None:
            return

        for column_number, column in enumerate(level.floor):
            for row_number, tile in enumerate(column):
                self.screen.addch(row_number + 1,
                                  column_number,
                                  ord(self.surface_manager.get_icon(tile)),
                                  self.surface_manager.get_attribute_by_name('dim'))

        for column_number, column in enumerate(level.walls):
            for row_number, tile in enumerate(column):
                glyph_number = self.surface_manager.get_icon(tile)
                if glyph_number is not None:
                    self.screen.addch(row_number + 1,
                                      column_number,
                                      ord(glyph_number),
                                      self.surface_manager.get_attribute_by_name('dim'))

        for portal in level.portals:
            self.screen.addch(portal.location[1] + 1,
                              portal.location[0],
                              ord(self.surface_manager.get_icon(portal.icon)),
                              self.surface_manager.get_attribute(portal.icon))

        for item in level.items:
            self.screen.addch(item.location[1] + 1,
                              item.location[0],
                              ord(self.surface_manager.get_icon(item.icon)),
                              self.surface_manager.get_attribute(item.icon))

        for monster in level.creatures:
            self.screen.addch(monster.location[1] + 1,
                              monster.location[0],
                              ord(self.surface_manager.get_icon(monster.icon)),
                              self.surface_manager.get_attribute(monster.icon))

        self.screen.addch(player.location[1] + 1,
                          player.location[0],
                          ord(self.surface_manager.get_icon(player.icon)),
                          self.surface_manager.get_attribute(player.icon))

        stats = 'HP:{0}({1}) MG:{2}({3})'.format(player.hit_points,
                                                 player.max_hp,
                                                 0,
                                                 0)
        stats = stats.ljust(80)
        self.screen.addstr(22, 0, stats)

        self.screen.refresh()

    @log_debug
    def receive_event(self, event):
        """
        Receive event
        """
        if event.event_type == 'move':
            self.refresh_screen()

            if event.mover == self.model.player:
                self.messages = []
                self.screen.addstr(0, 0, ' '.ljust(80))

        if e_event_type(event) in ['attack hit',
                                   'attack miss',
                                   'attack nothing',
                                   'poison triggered',
                                   'poison ended',
                                   'poisoned',
                                   'heal started',
                                   'heal ended',
                                   'heal triggered',
                                   'death',
                                   'pick up',
                                   'drop',
                                   'damage triggered',
                                   'equip',
                                   'unequip',
                                   'notice',
                                   'lose focus',
                                   'error']:
            message = event.get_description(self.model.player)
            self.messages.append(message)
            if len(self.messages) > 2:
                self.messages = self.messages[-2:]
            displayed_messages = ', '.join(self.messages)
            displayed_messages = displayed_messages.ljust(80)
            self.screen.addstr(0, 0, displayed_messages)

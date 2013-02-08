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
Module for map screen
"""
from pyherc.aspects import logged
from herculeum.ui.text.inventory import InventoryScreen
from herculeum.ui.text.character import CharacterScreen
from herculeum.ui.text.endscreen import EndScreen
from herculeum.ui.controllers import MoveController, EndScreenController

class MapScreen(object):
    """
    Class for map screen

    .. versionadded:: 0.9
    """
    @logged
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

    @logged
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
        for key in config.action_a:
            keymap[key] = self._action_a

        return keymap, move_keymap


    @logged
    def show(self):
        """
        Show the map
        """
        self.refresh_screen()
        player = self.model.player

        while self.model.end_condition == 0 and player.level != None:
            next_creature = self.model.get_next_creature(self.rules_engine)

            if next_creature == player:
                self._handle_player_input()
            else:
                next_creature.act(model = self.model,
                                  action_factory = self.action_factory,
                                  rng = self.rng)
            self.refresh_screen()

        dialog = EndScreen(model = self.model,
                           dying_rules = self.rules_engine.dying_rules,
                           screen = self.screen,
                           controller = EndScreenController())
        dialog.show()

    @logged
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
                self.model.player.perform_attack(direction,
                                                 self.action_factory,
                                                 self.rng)
        elif key == 'Q':
            self.model.end_condition = 1

    @logged
    def _move(self, key):
        """
        Process movement key

        :param key: key triggering the processing
        :type key: string
        """
        direction = self.move_key_map[key]
        self.move_controller.move_or_attack(self.model.player,
                                            direction,
                                            'walk')
    @logged
    def _action_a(self, key):
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

    @logged
    def refresh_screen(self):
        """
        Draw whole screen
        """
        player = self.model.player
        level = player.level

        if level == None:
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
                if glyph_number != None:
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

    @logged
    def receive_event(self, event):
        """
        Receive event
        """
        if event.event_type == 'move':
            self.refresh_screen()

            if event.mover == self.model.player:
                self.messages = []
                self.screen.addstr(0, 0, ' '.ljust(80))

        if event.event_type in ['attack hit',
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
                                    'lose focus']:
            message = event.get_description(self.model.player)
            self.messages.append(message)
            if len(self.messages) > 2:
                self.messages = self.messages[-2:]
            displayed_messages = ', '.join(self.messages)
            displayed_messages = displayed_messages.ljust(80)
            self.screen.addstr(0, 0, displayed_messages)

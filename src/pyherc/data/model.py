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
Module for Model related classes
"""

from pyherc.aspects import log_debug
from pyherc.data.level import get_characters
from pyherc.events import e_level

ESCAPED_DUNGEON = 1
DIED_IN_DUNGEON = 2


class Model():
    """
    Represents playing world
    """
    @log_debug
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.dungeon = None
        self.player = None
        self.config = None
        self.tables = None
        self.__event_listeners = []
        self.end_condition = 0

    @log_debug
    def register_event_listener(self, listener):
        """
        Registers event listener on this model

        :param listener: Listener to register
        """
        assert listener is not None
        self.__event_listeners.append(listener)

    @log_debug
    def get_event_listeners(self):
        """
        Retrieve registered event listeners
        """
        return self.__event_listeners[:]

    @log_debug
    def raise_event(self, event):
        """
        Relays event to creatures

        :param event: event to relay
        :type event: dict
        """
        level = e_level(event)

        if self.player:
            self.player.receive_event(event)

        for listener in self.__event_listeners:
            listener.receive_event(event)

    def get_next_creature(self, rules_engine):
        """
        Get the character who is next to take action

        :param rules_engine: engine containing rules
        :type rules_engine: RulesEngine
        :returns: Character to act next
        :rtype: Character
        """
        level = self.player.level

        if level is None:
            return None

        creatures = list(get_characters(level))

        while 1:
            for creature in creatures:
                if creature.tick <= 0:
                    return creature

            for creature in creatures:
                creature.tick = creature.tick - 1
                for effect in creature.get_effects():
                    if effect.tick is not None:
                        effect.tick = effect.tick - 1
                        if effect.tick <= 0:
                            effect.trigger(rules_engine.dying_rules)
                creature.remove_expired_effects()
                for skill, limit in creature.cooldowns.items():
                    if limit > 0:
                        creature.cooldowns[skill] = limit - 1


class Damage():
    """
    Damage done in combat
    """
    @log_debug
    def __init__(self, amount=0, damage_type='bludgeoning', magic_bonus=0):
        super().__init__()

        self.amount = amount
        self.damage_type = damage_type
        self.magic_bonus = magic_bonus


class MimicData():
    """
    Represents mimicing character
    """
    @log_debug
    def __init__(self, character):
        super().__init__()

        self.fov_matrix = []
        self.character = character

    @log_debug
    def get_character(self):
        """
        Get mimicing character

        :returns: Character
        :rtype: Character
        """
        return self.character

    @log_debug
    def set_character(self, character):
        """
        Set character mimicing this item

        :param character: Character to set
        :type character: Character
        """
        self.character = character

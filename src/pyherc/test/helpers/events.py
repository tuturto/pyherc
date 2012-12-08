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
Module for event helpers
"""
from pyherc.aspects import logged
from pyherc.data import Model
from pyherc.test.builders import ActionFactoryBuilder

def observed(fn):
    """
    Decorator to inject observer

    .. versionadded:: 0.8
    """
    def observe(*args, **kwargs):
        """
        Inject observer
        """
        context = args[0]

        if not hasattr(context, 'observer'):
            context.observer = EventListener()

            if not hasattr(context, 'model'):
                context.model = Model()

            context.model.register_event_listener(context.observer)

        return fn(*args, **kwargs)

    return observe

def with_action_factory(fn):
    """
    Decorator to inject action factory

    .. versionadded:: 0.8
    """
    def action_factorize(*args, **kwargs):
        """
        Inject action factory
        """
        context = args[0]

        if not hasattr(context, 'action_factory'):
            context.action_factory = (ActionFactoryBuilder()
                                            .with_move_factory()
                                            .with_attack_factory()
                                            .with_drink_factory()
                                            .with_inventory_factory()
                                            .with_dying_rules()
                                            .build())
        return fn(*args, **kwargs)

    return action_factorize

class EventListener(object):
    """
    Event listener that stores all events it receives
    """
    @logged
    def __init__(self):
        """
        Default constructor
        """
        super(EventListener, self).__init__()
        self.events = []

    @logged
    def receive_event(self, event):
        """
        Receive event

        :param event: event to receive
        :type event: Event
        """
        self.events.append(event)

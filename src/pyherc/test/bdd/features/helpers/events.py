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
Module for event helpers
"""
from pyherc.data import Model
from pyherc.test.builders import ActionFactoryBuilder
from pyherc.test.helpers import EventListener

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

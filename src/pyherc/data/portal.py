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
Module containing classes to represent Portals
"""

from pyherc.aspects import log_debug


class Portal():
    """
    Portal linking two levels together
    """
    @log_debug
    def __init__(self, icons, level_generator_name):
        """
        Default constructor

        :param icons: (my_icon, icon for other end)
        :type icons: (integer, integer)
        :param level_generator_name: name of level generator for proxy portals
        :type level_generator_name: String
        """
        super().__init__()
        self.level = None
        self.location = ()
        self.__icons = icons
        self.__other_end = None
        self.exits_dungeon = False
        self.level_generator_name = level_generator_name
        self.model = None
        self.__update_listeners = []

    @log_debug
    def get_other_end(self, level_generator_factory):
        """
        Returns the other end of the portal

        :param level_generator_factory: factory to generate level generators
        :type level_generator_factory: LevelGeneratorFactory
        :returns: other end of the portal
        :rtype: Portal
        """
        if self.__other_end is None:
            level_generator = level_generator_factory.get_generator(
                self.level_generator_name)
            level_generator(self)

        return self.__other_end

    @log_debug
    def set_other_end(self, portal):
        """
        Set the other end of the portal

        :param portal: portal where this one leads
        :type portal: Portal
        """
        self.__other_end = portal

    @log_debug
    def __get_icon(self):
        """
        Get icon to display this portal

        :returns: icon of the portal
        :rtype: integer
        """
        return self.__icons[0]

    @log_debug
    def __set_icon(self, icon):
        """
        Set icon to display this portal

        :param icon: icon to use for the portal
        :type icon: integer
        """
        if self.__icons is None:
            self.__icons = (None, None)
        self.__icons = (icon, self.__icons[1])

    @log_debug
    def __get_other_end_icon(self):
        """
        Get icon used for other end of this portal

        :returns: icon of the other end
        :rtype: integer
        """
        return self.__icons[1]

    @log_debug
    def register_for_updates(self, listener):
        """
        Register listener to receive updates for this entity

        :param listener: listener to add
        :type listener: Listener

        .. versionadded:: 0.5
        """
        self.__update_listeners.append(listener)

    @log_debug
    def remove_from_updates(self, listener):
        """
        Remove listener

        :param listener: listener to remove
        :type listener: Listener

        .. versionadded:: 0.5
        """
        self.__update_listeners.remove(listener)

    @log_debug
    def notify_update_listeners(self, event):
        """
        Notify all listeners registered for update of this entity

        :param event: event to relay to update listeners
        :type event: Event

        .. versionadded:: 0.5
        """
        for listener in self.__update_listeners:
            listener.receive_update(event)

    icon = property(__get_icon, __set_icon)
    other_end_icon = property(__get_other_end_icon)

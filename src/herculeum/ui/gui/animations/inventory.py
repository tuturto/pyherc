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
Classes for inventory animations
"""

from .animation import Animation
from herculeum.ui.gui.layers import zorder_item
from pyherc.events import e_item


class DropAnimation(Animation):
    """
    Generic animation for dropping item

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.item = e_item(event)

    def trigger(self, ui):
        """
        Trigger this animation
        """
        if (self.item.level):
            ui.add_glyph(self.item, ui.scene, zorder_item)


class PickUpAnimation(Animation):
    """
    Generic animation for picking up an item

    .. versionadded:: 0.12
    """
    def __init__(self, event):
        """
        Default constructor
        """
        super().__init__(event)

        self.item = e_item(event)

    def trigger(self, ui):
        """
        Trigger this animation
        """
        ui.remove_glyph(self.item)

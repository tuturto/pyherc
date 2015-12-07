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
Factory class for animations
"""

from .animation import Animation
from .attack import AttackHitAnimation
from .damage import DamageTriggeredAnimation
from .death import DeathAnimation
from .dig import DigAnimation
from .healing import HealAddedAnimation, HealTriggeredAnimation
from .inventory import DropAnimation, PickUpAnimation
from .metamorphosis import MetamorphosisAnimation
from .mitosis import MitosisAnimation
from .moving import MoveAnimation
from .perception import NoticeAnimation, LoseFocusAnimation
from .poison import PoisonAddedAnimation, PoisonTriggeredAnimation
from .trap import PlaceTrapAnimation
from pyherc.events import e_event_type

class AnimationFactory():
    """
    Class for creating animations for events

    .. versionadded:: 0.12
    """
    def __init__(self):
        """
        Default constructor
        """
        self.animations = {
            'attack hit': AttackHitAnimation,
            'damage triggered': DamageTriggeredAnimation,
            'death': DeathAnimation,
            'dig': DigAnimation,
            'drop': DropAnimation,
            'heal started': HealAddedAnimation,
            'heal triggered': HealTriggeredAnimation,
            'lose focus': LoseFocusAnimation,
            'metamorphosis': MetamorphosisAnimation,
            'mitosis': MitosisAnimation,
            'move': MoveAnimation,
            'notice': NoticeAnimation,
            'pick up': PickUpAnimation,
            'poisoned': PoisonAddedAnimation,
            'poison triggered': PoisonTriggeredAnimation,
            'trap placed': PlaceTrapAnimation
        }

    def create_animation(self, event):
        """
        Create an animation for event

        :param event: event to create animation for
        :type event: Event
        :returns: animation
        :rtype: Animation
        """
        if e_event_type(event) in self.animations:
            return self.animations[e_event_type(event)](event)
        else:
            return Animation(event)

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
Factory class for animations
"""

from .animation import Animation
from .attack import AttackHitAnimation
from .damage import DamageTriggeredAnimation
from .death import DeathAnimation
from .healing import HealAddedAnimation, HealTriggeredAnimation
from .inventory import DropAnimation, PickUpAnimation
from .metamorphosis import MetamorphosisAnimation
from .mitosis import MitosisAnimation
from .moving import MoveAnimation
from .perception import NoticeAnimation, LoseFocusAnimation
from .poison import PoisonAddedAnimation, PoisonTriggeredAnimation


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
            'poison triggered': PoisonTriggeredAnimation
        }

    def create_animation(self, event):
        """
        Create an animation for event

        :param event: event to create animation for
        :type event: Event
        :returns: animation
        :rtype: Animation
        """
        if event.event_type in self.animations:
            return self.animations[event.event_type](event)
        else:
            return Animation(event)

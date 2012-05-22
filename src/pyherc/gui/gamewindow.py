#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
Module main display
"""

import pgu.gui
import images
from pgu import tilevid

class GameWindow(pgu.gui.Container):
    pass

    def __init__(self,  application, screen, surface_manager, **params):
        """
        Initialises game window

        Args:
            application: instance of currently running application
            screen: display to draw onto
            surface_manager: SurfaceManager for graphics
        """
        super(GameWindow, self).__init__(**params)

        self.application = application
        self.screen = screen
        self.surface_manager = surface_manager
        self.set_layout()

    def set_layout(self):
        """
        Set layout of this screen
        """
        bg = pgu.gui.Image(
                self.surface_manager.get_image(
                        images.image_play_area))
        self.add(bg, 0, 0)

    def run(self):
        """
        Update screen
        """
        #self.screen.fill((0,0,0))
        #self.screen.paint(self.screen)
        #pygame.display.flip()

        # images  -- a dict for images to be put in.
        # tlayer  -- the foreground tiles layer
        # blayer  -- the background tiles layer (optional)
        assert 1 == 2
        self.tilevid.loop()

        updates = self.tilevid.update(self.tilevid.screen)
        pygame.display.update(updates)

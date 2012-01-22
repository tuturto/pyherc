import logging
import images
import pygame
import pyHerc
import pgu.gui
from pygame.locals import KEYDOWN
from pygame.locals import K_DOWN, K_UP
from pygame.locals import K_SPACE, K_RETURN, K_ESCAPE, K_PERIOD
from pygame.locals import K_d, K_w, K_r, K_q,  K_i
from pygame.locals import K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9
from pygame.locals import Rect

class StartMenu(pgu.gui.Container):
    """
    Start menu
    """

    def __init__(self,  application, screen, surface_manager, **params):
        """
        Initialises start menu
        @param application: instance of currently running application
        @param screen: display to draw onto
        """
        super(StartMenu, self).__init__(**params)

        self.running = 1
        self.selection = 0
        self.application = application
        self.screen = screen
        self.surface_manager = surface_manager
        self.logger = logging.getLogger('pyHerc.gui.windows.StartMenu')
        self.logger.debug('initialising start menu')

        self.set_layout()

        self.logger.debug('start menu initialised')

    def set_layout(self):
        '''
        Set layout of this screen
        '''
        b = pgu.gui.Button("New game", width=150)
        self.add(b, 0, 0)
        b.connect(pgu.gui.CLICK, self.__startNewGame, None)

        b = pgu.gui.Button("Load game", width=150)
        self.add(b, 0, 50)

        b = pgu.gui.Button("Quit", width=150)
        self.add(b, 0, 100)

    def __startNewGame(self, event_params):
        self.logger.info('starting a new game')
        newWindow = pyHerc.gui.windows.StartNewGameWindow(self.application, self.screen, self.surface_manager)
        newWindow.mainLoop()
        #TODO: world initialisation needs action factory
        #TODO: action factory needs world
        self.application.initialise_factories(self.application.world)

        self.application.world.player = newWindow.character
        newWindow = pyHerc.gui.windows.GameWindow(self.application, self.screen, self.surface_manager)
        newWindow.mainLoop()
        self.logger.info('game finished')
        if self.application.running:
            endResult = pyHerc.rules.ending.check_result(self.application.world)
            dialog = pyHerc.gui.dialogs.EndScreen(self.application, self.screen, self.surface_manager)
            dialog.show(endResult)

        self.repaint()

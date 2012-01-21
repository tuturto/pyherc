import logging
import images
import pygame
import pyHerc
from pygame.locals import KEYDOWN
from pygame.locals import K_DOWN, K_UP
from pygame.locals import K_SPACE, K_RETURN, K_ESCAPE, K_PERIOD
from pygame.locals import K_d, K_w, K_r, K_q,  K_i
from pygame.locals import K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9
from pygame.locals import Rect

class StartMenu:
    """
    Start menu
    """

    def __init__(self,  application, screen, surface_manager = None):
        """
        Initialises start menu
        @param application: instance of currently running application
        @param screen: display to draw onto
        """
        self.running = 1
        self.selection = 0
        self.application = application
        self.screen = screen
        self.logger = logging.getLogger('pyHerc.gui.windows.StartMenu')
        self.logger.debug('initialising start menu')

        self.surface_manager = surface_manager
        if self.surface_manager == None:
            self.logger.warn('Surface manager not specified, defaulting to the system one.')
            self.surface_manager = pyHerc.gui.surfaceManager.SurfaceManager()
            self.surface_manager.loadResources()

        self.background = self.surface_manager.getImage(images.image_start_menu)
        self.arrow = self.surface_manager.getImage(images.image_start_menu_arrow)

        self.arrow_location = [(275 - self.arrow.get_width(), 204 - self.arrow.get_height() / 2),
                                        (275 - self.arrow.get_width(), 310 - self.arrow.get_height() / 2),
                                        (275 - self.arrow.get_width(), 417 - self.arrow.get_height() / 2)]

        self.arrow_rects = [Rect(self.arrow_location[0], self.arrow.get_size()),
                                            Rect(self.arrow_location[1], self.arrow.get_size()),
                                            Rect(self.arrow_location[2], self.arrow.get_size())]

        #TODO: use configuration
        self.dirty_rectangles = [Rect(0, 0, 800, 600)]

        self.logger.debug('start menu initialised')

    def mainLoop(self):
        """
        This is the event handler for start menu
        """
        self.logger.debug('Main loop starting')
        while self.running and self.application.running:

            self.__updateDisplay()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.logger.info('Quit received, exiting')
                    self.running = 0
                if event.type == KEYDOWN:
                    if event.key in (K_DOWN, K_KP2):
                        self.dirty_rectangles.append(self.arrow_rects[self.selection])
                        self.selection = self.selection + 1
                        if self.selection > 2:
                            self.selection = 0
                        self.dirty_rectangles.append(self.arrow_rects[self.selection])
                    elif event.key in (K_UP, K_KP8):
                        self.dirty_rectangles.append(self.arrow_rects[self.selection])
                        self.selection = self.selection - 1
                        if self.selection < 0:
                            self.selection = 2
                        self.dirty_rectangles.append(self.arrow_rects[self.selection])
                    elif event.key in (K_SPACE, K_RETURN,  K_KP5):
                        if self.selection == 0:
                            self.logger.debug('new game selected')
                            self.__startNewGame()
                            self.dirty_rectangles = [Rect(0, 0, 800, 600)]
                        elif self.selection == 1:
                            self.logger.debug('load game selected')
                            #TODO: implement
                        elif self.selection == 2:
                            self.logger.debug('exit selected')
                            self.running = 0

        self.logger.debug('main loop finished')

    def __startNewGame(self):
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


    def __updateDisplay(self):
        """
        Draws this window on screen
        """
        if len(self.dirty_rectangles) > 0:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.arrow, self.arrow_location[self.selection])

            pygame.display.update(self.dirty_rectangles)
            self.dirty_rectangles = []

import logging
import images
import pygame
import pyherc
import pgu.gui

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
        self.logger = logging.getLogger('pyherc.gui.windows.StartMenu')
        self.logger.debug('initialising start menu')

        self.set_layout()

        self.logger.debug('start menu initialised')

    def set_layout(self):
        '''
        Set layout of this screen
        '''
        bg = pgu.gui.Image(
                                        self.surface_manager.getImage(images.image_start_menu))
        self.add(bg, 0, 0)

        b = pgu.gui.Button("New game", width=150)
        self.add(b, 325, 200)
        b.connect(pgu.gui.CLICK, self.__startNewGame)

        b = pgu.gui.Button("Load game", width=150)
        self.add(b, 325, 250)

        b = pgu.gui.Button("Quit", width=150)
        self.add(b, 325, 300)
        b.connect(pgu.gui.CLICK, self.__quit_game)

    def __startNewGame(self):
        self.logger.info('starting a new game')
        newWindow = pyherc.gui.windows.StartNewGameWindow(self.application, self.screen, self.surface_manager)
        newWindow.mainLoop()
        #TODO: world initialisation needs action factory
        #TODO: action factory needs world
        self.application.initialise_factories(self.application.world)

        self.application.world.player = newWindow.character
        newWindow = pyherc.gui.windows.GameWindow(self.application, self.screen, self.surface_manager)
        newWindow.mainLoop()
        self.logger.info('game finished')
        if self.application.running:
            endResult = pyherc.rules.ending.check_result(self.application.world)
            dialog = pyherc.gui.dialogs.EndScreen(self.application, self.screen, self.surface_manager)
            dialog.show(endResult)

        self.repaint()

    def __quit_game(self):
        self.get_toplevel().quit()

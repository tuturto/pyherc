'''
Display static image
'''

from pygame.locals import *

from .const import *
from . import widget, surface
from . import basic

class ImageBox(widget.Widget):

    def __init__(self, **params):
        widget.Widget.__init__(self,**params)
        self.image = None

    def paint(self, s):
        # Paint the pygame.Surface
        #if self.image != None and s != None:
        #    s.blit(self.image, s)
        pass
            
    def update(self, s):
        # Update the pygame.Surface and return the update rects
        return [pygame.Rect(0, 0, self.rect.w, self.rect.h)]
                
    def event(self, e):
        # Handle the pygame.Event
        return
                
    def resize(self, width=None, height=None):
        return self.rect.w,self.rect.h
    
    def set_image(self, image):
        self.image = image
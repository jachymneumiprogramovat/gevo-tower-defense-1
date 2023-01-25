from abc import ABC, abstractmethod
from pygame.sprite import RenderUpdates, spritecollideany, groupcollide, Sprite
from pygame import Surface, SCALED, Rect


class GameObject(Surface):
    """ The most general of the clases """
    
    def __init__(
        self, x:int, y:int, width:int, height:int, image:Surface
        ) -> None:

        self.rect=Rect(x,y,width,height)
        self.image=image

    def update(self)->None:    
        """update"""

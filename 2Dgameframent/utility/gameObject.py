import copy
import pygame

class Gameobject:
    def __init__(self,file):
        self.file=file
        self.image=pygame.image.load(f'{file}')

    def draw(self,rect,screen):
        screen.blit(self.image,rect)

    def drawTaskCell(self,rect,screen):
        lessenRect=pygame.Rect(rect)
        lessenRect.x=rect.x+4
        lessenRect.y=rect.y+4
        image=pygame.transform.scale(self.image,(22,22))
        screen.blit(image,lessenRect)

    def __deepcopy__(self, memodict={}):
        newOne=type(self)(copy.deepcopy(self.file,memodict))
        return newOne

    def __getstate__(self):
        state=self.__dict__.copy()
        del state["image"]
        return state
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image=pygame.image.load(f'{self.file}')
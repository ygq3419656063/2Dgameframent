from .baseClass import Game
import pygame
from tkinter import Tk, filedialog


class BgElement:
    def __init__(self,file,rect_x,rect_y):
        self.file=file
        self.image=pygame.image.load(file)
        rect=self.image.get_rect()
        self.rect=pygame.Rect(rect_x,rect_y,rect.width,rect.height)
        self.scale=1
        self.scaleImage=pygame.image.load(file)
        self.scaleRect=pygame.Rect(rect_x,rect_y,rect.width,rect.height)





    def __getstate__(self):
        state=self.__dict__.copy()
        del state["image"]
        del state["scaleImage"]
        return state
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image=pygame.image.load(f'{self.file}')
        self.scaleImage = pygame.transform.scale(self.image, (self.rect.width * self.scale, self.rect.height * self.scale))


    def draw(self):
        #Game.screen.blit(self.image,self.rect)
        self.scale=max(0.1,self.scale)
        self.scaleImage=pygame.transform.scale(self.image,(self.rect.width*self.scale,self.rect.height*self.scale))
        self.scaleRect.width=self.rect.width*self.scale
        self.scaleRect.height=self.rect.height*self.scale
        Game.screen.blit(self.scaleImage,self.scaleRect)


def loadBgElement():
    rect_x=Game.mouseLocation.normalScalex
    rect_y=Game.mouseLocation.normalScaley
    root = Tk()
    root.withdraw()
    # 选择文件
    file_path = filedialog.askopenfilename()
    if file_path:
        bgElemnt=BgElement(file_path,rect_x,rect_y)
        Game.imageLayer.bgImages.append(bgElemnt)
    #image = pygame.image.load(file_path)








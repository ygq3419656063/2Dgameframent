import sys
import pygame
from .set_parameter import SetParameter
#from .baseClass import Game

class ImageLayer:
    def __init__(self):
        self.Images=[]
        self.bgImages=[]
        self.dragElement=None
    def draw(self,Game):
        bg=pygame.image.load(f'picture//bg.jpg')
        #bg = pygame.transform.scale(bg, (SetParameter.windowsWidth, SetParameter.windowsHeight))
        bgrect = pygame.Rect((Game.crop_x, Game.crop_y), (SetParameter.windowsWidth, SetParameter.windowsHeight))
        Game.screen.blit(bg,(0,0),bgrect)
        for bgElement in self.bgImages:
            bgElement.draw()

        for i in range((Game.crop_y//SetParameter.cellSize),(Game.crop_y//SetParameter.cellSize)+(SetParameter.windowsHeight//SetParameter.cellSize)):
            for j in range((Game.crop_x//SetParameter.cellSize),(Game.crop_x//SetParameter.cellSize)+(SetParameter.windowsWidth//SetParameter.cellSize)):
                cell=Game.board.cellList[i][j]
                if cell.cellcontainer!=None:
                    Game.screen.blit(cell.cellcontainer.image,(j*SetParameter.cellSize-Game.crop_x,i*SetParameter.cellSize-Game.crop_y))
                if cell.NPC!=None:
                    if cell.NPC.animatorFrame!=None:
                        Game.screen.blit(cell.NPC.animatorFrame,cell.NPC.relativeRect)




        Game.taskbar.draw()

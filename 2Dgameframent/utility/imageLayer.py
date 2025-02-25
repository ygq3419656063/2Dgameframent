import sys
import pygame
from .set_parameter import SetParameter

class ImageLayer:
    def __init__(self):
        self.Images=[]
        self.bgImages=[]
        self.dragElement=None
        self.mapImage=pygame.image.load(f'picture//bg.jpg')
    def draw(self,Game):
        #bg=pygame.image.load(f'picture//bg.jpg')
        bgrect = pygame.Rect((Game.crop_x, Game.crop_y), (SetParameter.windowsWidth, SetParameter.windowsHeight))
        Game.screen.blit(self.mapImage,(0,0),bgrect)
        for bgElement in self.bgImages:
            bgElement.draw()

        #将npc放到一行的最后去渲染，保证渲染层次
        npcImage = []
        for i in range((Game.crop_y//SetParameter.cellSize),(Game.crop_y//SetParameter.cellSize)+(SetParameter.windowsHeight//SetParameter.cellSize)):
            for j in range((Game.crop_x//SetParameter.cellSize),(Game.crop_x//SetParameter.cellSize)+(SetParameter.windowsWidth//SetParameter.cellSize)):
                cell=Game.board.cellList[i][j]
                if cell.cellcontainer!=None:
                    Game.screen.blit(cell.cellcontainer.image,(j*SetParameter.cellSize-Game.crop_x,i*SetParameter.cellSize-Game.crop_y))
                if cell.NPC!=None:
                    npcImage.append(cell.NPC)
            for npc in npcImage:
                #if npc.animatorFrame != None:
                Game.screen.blit(npc.animatorFrame,npc.relativeRect)
            npcImage.clear()
        Game.taskbar.draw(Game)
        if Game.dialogue!=None:
            Game.dialogue.draw()

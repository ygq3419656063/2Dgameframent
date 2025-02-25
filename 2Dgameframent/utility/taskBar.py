import pygame
from .set_parameter import SetParameter
from .gameObject import Gameobject
import copy


class TaskBar:
    def __init__(self):
        self.boardwith=4
        self.equipmentList=[None for i in range(10)]
        self.rect=pygame.Rect(0,(SetParameter.windowsHeight//SetParameter.cellSize-1)*SetParameter.cellSize,10*SetParameter.cellSize,SetParameter.cellSize)
        cellobject0 = Gameobject(f'picture//ice.jpg')
        self.equipmentList[0]=cellobject0
        cellobject1=Gameobject(f'picture//umbrella.jpg')
        self.equipmentList[1]=cellobject1
        cellobject2=Gameobject(f'picture//heart.jpg')
        self.equipmentList[2]=cellobject2

    def update(self):
        self.rect = pygame.Rect(0, (SetParameter.windowsHeight // SetParameter.cellSize - 1) * SetParameter.cellSize,
                                10 * SetParameter.cellSize, SetParameter.cellSize)


    def draw(self,Game):
        i=0
        taskCell=pygame.Rect(0,(SetParameter.windowsHeight//SetParameter.cellSize-1)*SetParameter.cellSize,SetParameter.cellSize,SetParameter.cellSize)
        while i<10:
            pygame.draw.rect(Game.screen,SetParameter.colorRed,taskCell,self.boardwith)
            taskCell.x=taskCell.x+SetParameter.cellSize
            i=i+1

        taskCell = pygame.Rect(0,
                               (SetParameter.windowsHeight // SetParameter.cellSize - 1) * SetParameter.cellSize,
                               SetParameter.cellSize, SetParameter.cellSize)
        for index,equipment in enumerate(self.equipmentList):
            if equipment!=None:
                self.equipmentList[index].drawTaskCell(taskCell,Game.screen)
                taskCell.x = taskCell.x + SetParameter.cellSize

    def isHover(self,Game):
        pygame.draw.rect(Game.screen,SetParameter.colorBlack,(Game.mouseLocation.normalScalex,Game.mouseLocation.normalScaley,SetParameter.cellSize,SetParameter.cellSize),self.boardwith)


    def chosen(self,Game):
        i=(Game.mouseLocation.normalScalex-self.rect.x)//SetParameter.cellSize
        if self.equipmentList[i]!=None:
            Game.player.handThing=copy.deepcopy(self.equipmentList[i])
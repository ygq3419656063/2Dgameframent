import enum
import pygame
import copy
import threading
from .animator import PersonState
import time
import pickle

class SetParameter:
    windowsWidth=900
    windowsHeight=600
    colorBlack=(0,0,0)
    colorWhite=(255,255,255)
    colorRed=(255,0,0)
    cellSize=30




class Game:
    board=None
    player=None
    imageLayer=None
    screen=None
    player=None
    mouseLocation=None
    taskbar=None
    @classmethod
    def save(cls):
        with open(f'historyfile//player.pkl',"wb") as file:
            pickle.dump(cls.player.rect,file)
        with open(f'historyfile//boardCellList.pkl',"wb") as file:
            pickle.dump(cls.board.cellList,file)

    @classmethod
    def load(cls):
        with open(f"historyfile//player.pkl", "rb") as file:
            cls.player.rect=pickle.load(file)
        with open(f"historyfile//boardCellList.pkl","rb") as file:
            cls.board.cellList=pickle.load(file)



    @classmethod
    def isHover(cls):
        if cls.mouseLocation.TaskBarLoction:
            cls.taskbar.isHover()
        elif cls.mouseLocation.BackGroundLocation:
            cls.board.is_hover()

    @classmethod
    def mouseLeftHit(cls):
        if cls.mouseLocation.TaskBarLoction:
            cls.taskbar.chosen()

    @classmethod
    def mouseRightHit(cls):
        if cls.mouseLocation.BackGroundLocation:
            cls.board.is_hit()



class Cell:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.cellcontainer=None

class Board:
    def __init__(self):
        self.rect=pygame.Rect(0,0,SetParameter.windowsWidth,SetParameter.windowsHeight)

        self.cellList=[[None for j in range(SetParameter.windowsWidth//SetParameter.cellSize)] for i in range(SetParameter.windowsHeight//SetParameter.cellSize)]
    def init(self):
        for i in range(SetParameter.windowsHeight//SetParameter.cellSize):
            for j in range(SetParameter.windowsWidth//SetParameter.cellSize):
                cell=Cell(i,j)
                self.cellList[i][j]=cell
    def is_hover(self):

        x=Game.mouseLocation.normalScalex
        y=Game.mouseLocation.normalScaley
        hoverSurface = pygame.Surface((SetParameter.cellSize, SetParameter.cellSize), pygame.SRCALPHA)
        hoverSurface.fill((255, 0, 0, 128))
        Game.screen.blit(hoverSurface,(x,y))

    def is_hit(self):
        if Game.player.handThing!=None:
            cellobject=copy.deepcopy(Game.player.handThing)
            x = Game.mouseLocation.normalx
            y = Game.mouseLocation.normaly
            self.cellList[y][x].cellcontainer=cellobject
            #Game.imageLayer.Images.append((cellobject.image,(x*SetParameter.cellSize,y*SetParameter.cellSize)))

    def draw(self):
        for y in range(len(self.cellList)):
            for x in range(len(self.cellList[0])):
                if self.cellList[y][x]!=None:
                    if self.cellList[y][x].cellcontainer!=None:
                        Game.screen.blit(self.cellList[y][x].cellcontainer.image,(x*SetParameter.cellSize,y*SetParameter.cellSize))



class ImageLayer:
    def __init__(self):
        self.Images=[]
    def draw(self):
        bg=pygame.image.load(f'picture//background.webp')
        bg = pygame.transform.scale(bg, (SetParameter.windowsWidth, SetParameter.windowsHeight))
        bgrect = pygame.Rect((0, 0), (SetParameter.windowsWidth, SetParameter.windowsHeight))
        Game.screen.blit(bg,bgrect)
        Game.board.draw()
        for image in self.Images:
            Game.screen.blit(image[0],(image[1][0],image[1][1]))
        Game.taskbar.draw()
        if Game.player.animatorFrame!=None:
            Game.screen.blit(Game.player.animatorFrame,Game.player.rect)

class Gameobject:
    def __init__(self,file):
        self.file=file
        self.image=pygame.image.load(f'{file}')

    def draw(self,rect):
        Game.screen.blit(self.image,rect)

    def drawTaskCell(self,rect):
        lessenRect=pygame.Rect(rect)
        lessenRect.x=rect.x+4
        lessenRect.y=rect.y+4
        image=pygame.transform.scale(self.image,(22,22))
        Game.screen.blit(image,lessenRect)

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

class Player(threading.Thread):
    def __init__(self):
        super().__init__()
        self.handThing=None
        self.animatorFrame=None
        self.rect=pygame.Rect(0,0,30,60)
        self.animator=None
        self.running=True

    def run(self):
        while self.running:
            if Game.player.animator.state==PersonState.right:
                self.rect.x+=5
            elif Game.player.animator.state==PersonState.left:
                self.rect.x-=5
            elif Game.player.animator.state==PersonState.up:
                self.rect.y-=5
            elif Game.player.animator.state==PersonState.down:
                self.rect.y+=5
            time.sleep(0.1)

    def stop(self):
        self.running=False




class TaskBar:
    def __init__(self):
        self.boardwith=4
        self.equipmentList=[None for i in range(10)]
        self.rect=pygame.Rect(10*SetParameter.cellSize,(SetParameter.windowsHeight//SetParameter.cellSize-1)*SetParameter.cellSize,10*SetParameter.cellSize,SetParameter.cellSize)
        cellobject0 = Gameobject(f'picture//ice.jpg')
        self.equipmentList[0]=cellobject0
        cellobject1=Gameobject(f'picture//umbrella.jpg')
        self.equipmentList[1]=cellobject1
        cellobject2=Gameobject(f'picture//heart.jpg')
        self.equipmentList[2]=cellobject2

    def draw(self):
        i=0
        taskCell=pygame.Rect(10*SetParameter.cellSize,(SetParameter.windowsHeight//SetParameter.cellSize-1)*SetParameter.cellSize,SetParameter.cellSize,SetParameter.cellSize)
        while i<10:
            pygame.draw.rect(Game.screen,SetParameter.colorRed,taskCell,self.boardwith)
            #if self.equipmentList[i]!=None:
                #self.equipmentList[i].drawTaskCell(taskCell)
            taskCell.x=taskCell.x+SetParameter.cellSize
            i=i+1

        taskCell = pygame.Rect(10 * SetParameter.cellSize,
                               (SetParameter.windowsHeight // SetParameter.cellSize - 1) * SetParameter.cellSize,
                               SetParameter.cellSize, SetParameter.cellSize)
        for index,equipment in enumerate(self.equipmentList):
            if equipment!=None:
                self.equipmentList[index].drawTaskCell(taskCell)
                taskCell.x = taskCell.x + SetParameter.cellSize

    def isHover(self):
        pygame.draw.rect(Game.screen,SetParameter.colorBlack,(Game.mouseLocation.normalScalex,Game.mouseLocation.normalScaley,SetParameter.cellSize,SetParameter.cellSize),self.boardwith)


    def chosen(self):
        i=(Game.mouseLocation.normalScalex-self.rect.x)//SetParameter.cellSize
        if self.equipmentList[i]!=None:
            Game.player.handThing=copy.deepcopy(self.equipmentList[i])






class MouseLocation:
    def __init__(self):
        self.TaskBarLoction=False
        self.CellContainerLocation=False
        self.BackGroundLocation=False
        self.x=0
        self.y=0
        self.normalx=0
        self.normaly=0
        self.normalScalex=0
        self.normalScaley=0



    def location(self,mouse_pos):
        self.TaskBarLoction=False
        self.CellContainerLocation=False
        self.BackGroundLocation=False
        x=mouse_pos[0]//SetParameter.cellSize
        y=mouse_pos[1]//SetParameter.cellSize
        self.normalx=x
        self.normaly=y
        self.normalScalex=x*SetParameter.cellSize
        self.normalScaley=y*SetParameter.cellSize
        self.x=mouse_pos[0]
        self.y=mouse_pos[1]

        if Game.taskbar.rect.collidepoint(mouse_pos):
            self.TaskBarLoction=True
        elif Game.board.cellList[y][x].cellcontainer!=None:
            self.CellContainerLocation=True
        else:
            self.BackGroundLocation=True














import os
import pygame
import copy
import threading
from .animator import PersonState
import time
import pickle
from .role import  Role
from .set_parameter import SetParameter
from .imageLayer import ImageLayer
from .animator import Animator
from queue import Queue
from .gameConsole import GameConsole

class Game:
    board=None
    player=None
    imageLayer=None
    screen=None
    player=None
    mouseLocation=None
    taskbar=None
    npc=None
    npcs={}
    crop_x=0
    crop_y=0
    consoleQueue=None
    gameConsole=None
    isConsoling=False
    @classmethod
    def save(cls):
        with open(f'historyfile//player.pkl',"wb") as file:
            pickle.dump(cls.player.rect,file)
        with open(f'historyfile//boardCellList.pkl',"wb") as file:
            pickle.dump(cls.board.cellList,file)
        with open(f'historyfile//bgElements.pkl',"wb") as file:
            pickle.dump(cls.imageLayer.bgImages,file)

    @classmethod
    def load(cls):
        with open(f"historyfile//player.pkl", "rb") as file:
            cls.player.rect=pickle.load(file)
        with open(f"historyfile//boardCellList.pkl","rb") as file:
            cls.board.cellList=pickle.load(file)
        with open(f'historyfile//bgElements.pkl',"rb") as file:
            cls.imageLayer.bgImages=pickle.load(file)


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

    @classmethod
    def init(cls):

        Game.player = Player()
        Game.board = Board()
        Game.board.init()
        Game.board.cellList[0][0].NPC = Game.player
        Game.mouseLocation = MouseLocation()
        Game.taskbar = TaskBar()
        Game.screen = pygame.display.set_mode((SetParameter.windowsWidth, SetParameter.windowsHeight))
        Game.imageLayer = ImageLayer()
        AbiPiPath=f'E://gitrepository//2Dgameframent//picture//Abigail'
        abiAnimator=Animator(Game.player,os.path.join(AbiPiPath,f'quiet'),os.path.join(AbiPiPath,f'up'),os.path.join(AbiPiPath,f'down'),
                             os.path.join(AbiPiPath,f'left'),os.path.join(AbiPiPath,f'right'))
        Game.player.animator = abiAnimator
        abiAnimator.start()
        Game.npc = NPC(Role.abi)
        NpcAnimator=Animator(Game.npc,os.path.join(AbiPiPath,f'quiet'),os.path.join(AbiPiPath,f'up'),os.path.join(AbiPiPath,f'down'),
                             os.path.join(AbiPiPath,f'left'),os.path.join(AbiPiPath,f'right'))

        Game.npc.animator = NpcAnimator
        NpcAnimator.start()
        Game.npcs[Role.player] = Game.player
        Game.npcs[Role.abi] = Game.npc
        Game.player.start()

    @classmethod
    def stop(cls):
        Game.player.animator.stop()
        Game.npc.animator.stop()
        Game.player.stop()

    @classmethod
    def draw(cls):
        cls.imageLayer.draw(cls)

    @classmethod
    def startConsole(cls):
        cls.isConsoling=True
        consoleQueue=Queue()
        gameConsole=GameConsole(consoleQueue,cls)
        gameConsole.start()


    @classmethod
    def handleConsole(cls):
        while not cls.consoleQueue.empty():
            cmd = cls.consoleQueue.get()
            parts = cmd.strip().split()
            if not parts:
                continue

            command = parts[0].lower()
            args = parts[1:]

            if command == "viewwindow":
                if len(args) != 2:
                    print("参数错误！用法：viewWindow [width] [height]")
                    continue

                try:
                    new_width = int(args[0])
                    new_height = int(args[1])
                    if new_width < 100 or new_height < 100:
                        print("尺寸不能小于100x100！")
                        continue

                    cls.screen = pygame.display.set_mode(
                        (new_width, new_height)
                    )
                    SetParameter.windowsWidth=new_width
                    SetParameter.windowsHeight=new_height
                    print(f"窗口尺寸已调整为 {new_width}x{new_height}")
                except ValueError:
                    print("无效的尺寸参数！必须为整数")

            elif command == "exit":
                cls.gameConsole.stop()
                cls.isConsoling=False
            else:
                print(f"未知命令：{command}")







class Cell:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.cellcontainer=None
        self.NPC=None
        self.npcRole=None
    def __getstate__(self):
        if self.NPC !=None:
            self.npcRole = self.NPC.role
        state = self.__dict__.copy()
        if self.NPC!=None:
            del state["NPC"]

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        if self.npcRole!=None:
            self.NPC=Game.npcs[self.npcRole]


class Board:
    def __init__(self):
        self.rect=pygame.Rect(0,0,SetParameter.windowsWidth,SetParameter.windowsHeight)

        self.cellList=[[None for j in range(SetParameter.globalWindowWidth//SetParameter.cellSize)] for i in range(SetParameter.globalWindowHeight//SetParameter.cellSize)]
        self.rects=[]
    def init(self):
        for i in range(len(self.cellList)):
            for j in range(len(self.cellList[0])):
                cell=Cell(i,j)
                self.cellList[i][j]=cell



    def is_hover(self):
        x=Game.mouseLocation.globalNormalScalex-Game.crop_x
        y=Game.mouseLocation.globalNormalScaley-Game.crop_y
        hoverSurface = pygame.Surface((SetParameter.cellSize, SetParameter.cellSize), pygame.SRCALPHA)
        hoverSurface.fill((255, 0, 0, 128))
        Game.screen.blit(hoverSurface,(x,y))

    def is_hit(self):
        if Game.player.handThing!=None:
            cellobject=copy.deepcopy(Game.player.handThing)
            x = Game.mouseLocation.globalNormalx
            y = Game.mouseLocation.globalNormaly
            self.cellList[y][x].cellcontainer=cellobject

    def draw(self):
        for y in range(len(self.cellList)):
            for x in range(len(self.cellList[0])):
                if self.cellList[y][x]!=None:
                    if self.cellList[y][x].cellcontainer!=None:
                        Game.screen.blit(self.cellList[y][x].cellcontainer.image,(x*SetParameter.cellSize-Game.crop_x,y*SetParameter.cellSize-Game.crop_y))





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
        self.rect=pygame.Rect(300,300,30,30)
        self.animator=None
        self.running=True
        self.role=Role.player
        self.relativeRect=pygame.Rect(180,180,30,30)
        self.hasMoved=False



    def run(self):
        while self.running:
            oldCellIndex=(self.rect.x//SetParameter.cellSize,self.rect.y//SetParameter.cellSize)
            oldRect=pygame.Rect(self.rect)
            if Game.player.animator.state==PersonState.right:
                self.rect.x+=5
            elif Game.player.animator.state==PersonState.left:
                self.rect.x-=5
            elif Game.player.animator.state==PersonState.up:
                self.rect.y-=5
            elif Game.player.animator.state==PersonState.down:
                self.rect.y+=5
            newCellIndex=(self.rect.x//SetParameter.cellSize,self.rect.y//SetParameter.cellSize)
            cell=Game.board.cellList[newCellIndex[1]][newCellIndex[0]]
            if self.rect.collidelist(Game.board.rects)==-1:
                if oldCellIndex!=newCellIndex:
                    cell.NPC=self
                    Game.board.cellList[oldCellIndex[1]][oldCellIndex[0]].NPC = None
            else:
                self.rect = pygame.Rect(oldRect)
            time.sleep(0.1)

            cropold_x=Game.crop_x
            cropold_y=Game.crop_y
            if self.rect.x==oldRect.x and self.rect.y==oldRect.y:
                self.hasMoved=False
            else:
                self.hasMoved=True
            if self.hasMoved:
                if Game.player.animator.state==PersonState.right:
                    Game.crop_x+=5
                elif Game.player.animator.state==PersonState.left:
                    Game.crop_x-=5
                elif Game.player.animator.state==PersonState.up:
                    Game.crop_y-=5
                elif Game.player.animator.state==PersonState.down:
                    Game.crop_y+=5

            if Game.crop_x<0 or Game.crop_x>(1200-900):
                Game.crop_x=cropold_x
            if Game.crop_y<0 or Game.crop_y>(800-600):
                Game.crop_y=cropold_y

            Game.offset=[Game.crop_x,Game.crop_y]

            Game.npc.relativeRect.x=Game.npc.globalRect.x-Game.crop_x
            Game.npc.relativeRect.y=Game.npc.globalRect.y-Game.crop_y
            self.relativeRect.x=self.rect.x-Game.crop_x
            self.relativeRect.y=self.rect.y-Game.crop_y





    def stop(self):
        self.running=False

class NPC:
    def __init__(self,role):
        self.relativeRect=pygame.Rect(150,150,30,30)
        self.globalRect=pygame.Rect(150,150,30,30)
        self.cell = (self.globalRect.x // SetParameter.cellSize,
                     self.globalRect.y // SetParameter.cellSize )
        self.role=role
        Game.board.cellList[self.cell[1]][self.cell[0]].NPC=self
        self.animator=None
        self.animatorFrame = None
        Game.board.rects.append(self.globalRect)

        self.running=True










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
        self.globalx=0
        self.globaly=0
        self.globalNormalx=0
        self.globalNormaly=0
        self.globalNormalScalex=0
        self.globalNormalScaley=0



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

        self.globalx=mouse_pos[0]+Game.crop_x
        self.globaly=mouse_pos[1]+Game.crop_y
        self.globalNormalx=self.globalx//SetParameter.cellSize
        self.globalNormaly=self.globaly//SetParameter.cellSize
        self.globalNormalScalex=self.globalNormalx*SetParameter.cellSize
        self.globalNormalScaley=self.globalNormaly*SetParameter.cellSize




        if Game.taskbar.rect.collidepoint(mouse_pos):
            self.TaskBarLoction=True
        elif Game.board.cellList[y][x].cellcontainer!=None:
            self.CellContainerLocation=True
        else:
            self.BackGroundLocation=True














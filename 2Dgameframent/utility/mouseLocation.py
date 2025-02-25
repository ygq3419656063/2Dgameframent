from .set_parameter import SetParameter
class MouseLocation:
    def __init__(self,Game):
        self.TaskBarLoction=False
        self.CellContainerLocation=False
        self.BackGroundLocation=False
        self.npcLocation=False
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
        self.Game=Game


    def location(self,mouse_pos):
        self.TaskBarLoction=False
        self.CellContainerLocation=False
        self.BackGroundLocation=False
        self.npcLocation=False
        x=mouse_pos[0]//SetParameter.cellSize
        y=mouse_pos[1]//SetParameter.cellSize
        self.normalx=x
        self.normaly=y
        self.normalScalex=x*SetParameter.cellSize
        self.normalScaley=y*SetParameter.cellSize
        self.x=mouse_pos[0]
        self.y=mouse_pos[1]

        self.globalx=mouse_pos[0]+self.Game.crop_x
        self.globaly=mouse_pos[1]+self.Game.crop_y
        self.globalNormalx=self.globalx//SetParameter.cellSize
        self.globalNormaly=self.globaly//SetParameter.cellSize
        self.globalNormalScalex=self.globalNormalx*SetParameter.cellSize
        self.globalNormalScaley=self.globalNormaly*SetParameter.cellSize




        if self.Game.taskbar.rect.collidepoint(mouse_pos):
            self.TaskBarLoction=True
        elif self.Game.board.cellList[y][x].cellcontainer!=None:
            self.CellContainerLocation=True
        elif self.Game.npc.relativeRect.collidepoint(mouse_pos):
            self.npcLocation=True
        else:
            self.BackGroundLocation=True
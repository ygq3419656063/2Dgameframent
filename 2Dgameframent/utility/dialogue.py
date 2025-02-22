import os
from threading import Thread
import pygame
from utility.set_parameter import SetParameter
import time


class Dialogue(Thread):
    def __init__(self,profile,textfile,game):
        super().__init__()
        self.profile=profile
        self.textfile=textfile
        self.running=True
        self.game=game
        self.text=None
        self.profileImage=None
        self.pageTurn=True


    def draw(self):
        pygame.draw.rect(self.game.screen,(255,255,208),(0,SetParameter.windowsHeight-100,SetParameter.windowsWidth,100))
        if self.profileImage!=None:
            self.game.screen.blit(self.profileImage,(0,SetParameter.windowsHeight-100,100,100))
        if self.text!=None:
            self.game.screen.blit(self.text,(100,SetParameter.windowsHeight-50))



    def run(self):
        texts = []
        dialoguePtr=0
        self.profileImage=pygame.image.load(self.profile)
        # 检查文件是否存在
        if os.path.exists(self.textfile):
            with open(self.textfile, 'r', encoding='utf-8') as file:
                for line in file:
                    texts.append(line.strip())
        else:
            print(f"文件 {self.running} 不存在")
        font = pygame.font.Font("font//msyhl.ttc", 36)
        dialogue = texts[dialoguePtr]
        self.text = font.render(f'{dialogue}', True, (0, 0, 0))

        while self.running:
            if dialoguePtr >= len(texts):
                self.running = False
                self.game.dialogue=None
            if dialoguePtr <len(texts):
                if self.pageTurn==True:
                    dialogue = texts[dialoguePtr]
                    self.text = font.render(f'{dialogue}', True, (0, 0, 0))
                    time.sleep(1)
                    if dialoguePtr==0:
                        self.pageTurn=False
                    dialoguePtr+=1
                    if dialoguePtr==len(texts):
                        time.sleep(3)


    def stop(self):
        self.running=False









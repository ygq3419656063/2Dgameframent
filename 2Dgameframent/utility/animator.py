from enum import Enum,auto
import pygame
import os
import threading
import time
class PersonState(Enum):
    quiet=auto()
    left=auto()
    right=auto()
    up=auto()
    down=auto()

class Animator(threading.Thread):
    def __init__(self,npc,file1,file2,file3,file4,file5):
        super().__init__()
        self.npc=npc
        self.quiet = [pygame.image.load(os.path.join(file1, i)) for i in os.listdir(file1)]
        self.up=[pygame.image.load(os.path.join(file2,i)) for i in os.listdir(file2)]
        self.down=[pygame.image.load(os.path.join(file3,i)) for i in os.listdir(file3)]
        self.left=[pygame.image.load(os.path.join(file4,i)) for i in os.listdir(file4)]
        self.right = [pygame.image.load(os.path.join(file5, i)) for i in os.listdir(file5)]
        self.state=PersonState.quiet
        self.oldstate=PersonState.quiet
        self.running = True
        self.currentFrame = 0
        self.fps=10
    def run(self):
        while self.running:
            if self.state!=self.oldstate:
                self.oldstate=self.state
                self.currentFrame=0
            if self.state==PersonState.quiet:
                self.currentFrame=(self.currentFrame+1)%len(self.quiet)
                self.npc.animatorFrame=self.quiet[self.currentFrame]
            if self.state==PersonState.right:
                self.currentFrame = (self.currentFrame + 1) % len(self.right)
                self.npc.animatorFrame=self.right[self.currentFrame]
            if self.state==PersonState.left:
                self.currentFrame=(self.currentFrame+1) % len(self.left)
                self.npc.animatorFrame=self.left[self.currentFrame]
            if self.state==PersonState.up:
                self.currentFrame=(self.currentFrame+1) % len(self.up)
                self.npc.animatorFrame=self.up[self.currentFrame]
            if self.state==PersonState.down:
                self.currentFrame=(self.currentFrame+1) % len(self.down)
                self.npc.animatorFrame=self.down[self.currentFrame]
            time.sleep(1/self.fps)
    def stop(self):
        self.running=False











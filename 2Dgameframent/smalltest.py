'''


import pygame
from queue import  Queue
from threading import Thread
from utility.set_parameter import SetParameter
import os

class GameConsole(Thread):
    def __init__(self,queue):
        super().__init__()
        self.running = True
        self.queue=queue


    def run(self):
        while self.running:
            try:
                cmd = input(">>> ")
                self.queue.put(cmd)
            except EOFError:
                break

    def stop(self):
        self.running = False




# 假设你的TXT文件路径是 'example.txt'
file_path = 'dialogue//abi.txt'
texts=[]

# 检查文件是否存在
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            #print(line.strip())  # 使用 strip() 去除每行末尾的换行符
            texts.append(line.strip())
else:
    print(f"文件 {file_path} 不存在")

queue=Queue()
pygame.init()
screen=pygame.display.set_mode((SetParameter.windowsWidth, SetParameter.windowsHeight))
clock = pygame.time.Clock()
running = True
gameConsole=GameConsole(queue)
gameConsole.start()
rgbR=255
rgbG=255
rgbB=208
font=pygame.font.Font("font//msyhl.ttc",36)
dialoguePtr=0
dialogue=texts[dialoguePtr]
text=font.render(f'{dialogue}',True,(0,0,0))
profile=pygame.image.load(f'E://gitrepository//2Dgameframent//picture//Abigail//profile.jpg')
while running:
    while not queue.empty():
        cmd = queue.get()
        parts = cmd.strip().split()
        rgbR=int(parts[0])
        rgbG=int(parts[1])
        rgbB=int(parts[2])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==3:
                dialoguePtr+=1
                dialogue = texts[dialoguePtr]
                text = font.render(f'{dialogue}', True, (0, 0, 0))

    screen.fill((255,255,255))
    pygame.draw.rect(screen,(rgbR,rgbG,rgbB),(0,SetParameter.windowsHeight-100,SetParameter.windowsWidth,100))
    screen.blit(profile, (0, SetParameter.windowsHeight - 100, 100, 100))
    screen.blit(text,(100,SetParameter.windowsHeight-50))
    pygame.display.flip()
    clock.tick(60)
gameConsole.stop()
pygame.quit()
'''

#testRect=pygame.Rect(100,100,100,100)

'''
data={"left": 505, "top": 330, "width": 30, "height": 30}
readData={}
with open(f"historyfile//test.json","w") as file:
    json.dump(data,file)
with open(f"historyfile//test.json","r") as file:
    readData=json.load(file)
testRect=pygame.Rect(readData["left"],readData["top"],readData["width"],readData["height"])
print(testRect)
'''

import pygame
import json
from utility.role import  Role






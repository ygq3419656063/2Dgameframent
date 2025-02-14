

import pygame
from tkinter import Tk, filedialog

# 初始化Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Map Editor")

# 初始化Tkinter（隐藏主窗口）
root = Tk()
root.withdraw()

# 选择文件
file_path = filedialog.askopenfilename()
if file_path:
    image = pygame.image.load(file_path)
else:
    pygame.quit()
    exit()

# 设置初始位置和拖动状态
image_rect = image.get_rect()
image_rect.topleft = (100, 100)
dragging = False
offset_x = 0
offset_y = 0

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if image_rect.collidepoint(event.pos):
                dragging = True
                mouse_x, mouse_y = event.pos
                offset_x = image_rect.x - mouse_x
                offset_y = image_rect.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                image_rect.x = mouse_x + offset_x
                image_rect.y = mouse_y + offset_y

    screen.fill((255, 255, 255))  # 填充背景色
    screen.blit(image, image_rect.topleft)  # 绘制图片
    pygame.display.flip()

pygame.quit()




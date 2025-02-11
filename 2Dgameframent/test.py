from utility.baseClass  import *
from utility.animator import *
from utility.role import *



if __name__=="__main__":
    Game.player=Player()
    Game.board=Board()
    Game.board.init()
    Game.board.cellList[0][0].NPC=Game.player
    Game.mouseLocation=MouseLocation()
    Game.taskbar=TaskBar()
    Game.screen=pygame.display.set_mode((SetParameter.windowsWidth,SetParameter.windowsHeight))
    Game.imageLayer = ImageLayer()
    abiAnimator=Animator(Game.player,f'picture//Abigail//quiet',f'picture//Abigail//up',f'picture//Abigail//down',f'picture//Abigail//left',f'picture//Abigail//right')
    Game.player.animator=abiAnimator
    abiAnimator.start()
    Game.npc = NPC(Role.abi)
    NpcAnimator=Animator(Game.npc,f'picture//Abigail//quiet',f'picture//Abigail//up',f'picture//Abigail//down',f'picture//Abigail//left',f'picture//Abigail//right')
    Game.npc.animator=NpcAnimator
    NpcAnimator.start()


    Game.player.start()
    clock = pygame.time.Clock()
    running = True
    while running:

        Game.imageLayer.draw()
        mouse_pos = pygame.mouse.get_pos()
        Game.mouseLocation.location(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==3:
                    Game.mouseRightHit()
                if event.button==1:
                    Game.mouseLeftHit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_d:
                    for i in range(len(Game.board.cellList)):
                        for j in range(len(Game.board.cellList[0])):
                            if Game.board.cellList[i][j].NPC != None:
                                print((i, j),Game.board.cellList[i][j].NPC.role)
                if event.key==pygame.K_RIGHT:
                    Game.player.animator.state=PersonState.right
                elif event.key==pygame.K_LEFT:
                    Game.player.animator.state=PersonState.left
                elif event.key==pygame.K_UP:
                    Game.player.animator.state=PersonState.up
                elif event.key==pygame.K_DOWN:
                    Game.player.animator.state=PersonState.down
                elif event.key==pygame.K_k:
                    print("yes,k is pressed")
                    Game.save()
                elif event.key==pygame.K_l:
                    Game.load()


            elif event.type==pygame.KEYUP:
                if event.key == pygame.K_RIGHT or \
                        event.key == pygame.K_LEFT or \
                        event.key == pygame.K_UP or \
                        event.key == pygame.K_DOWN:
                    Game.player.animator.state=PersonState.quiet

        Game.isHover()
        pygame.display.flip()
        clock.tick(60)
    Game.player.animator.stop()
    Game.npc.animator.stop()
    Game.player.stop()

    pygame.quit()


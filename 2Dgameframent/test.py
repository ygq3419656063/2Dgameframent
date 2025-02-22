from utility.baseClass  import Game
from utility.animator import *
from utility.mapmaker import loadBgElement


if __name__=="__main__":
    Game.init()
    offset_x=0
    offset_y=0
    clock = pygame.time.Clock()
    running = True
    dragging=False
    while running:
        Game.draw()
        mouse_pos = pygame.mouse.get_pos()
        Game.mouseLocation.location(mouse_pos)
        Game.update()
        if Game.isConsoling==True:
            Game.handleConsole()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==3:
                    Game.mouseRightHit()
                if event.button==1:
                    for bgElement in Game.imageLayer.bgImages:
                        if bgElement.scaleRect.collidepoint(event.pos):
                            dragging=True
                            Game.imageLayer.dragElement=bgElement
                            mouse_x,mouse_y=event.pos
                            offset_x=bgElement.scaleRect.x-mouse_x
                            offset_y=bgElement.scaleRect.y-mouse_y
                    if not dragging:
                        Game.mouseLeftHit()
            elif event.type==pygame.MOUSEBUTTONUP:
                    if event.button==1:
                        dragging=False
                    if event.button==3:
                        Game.mouseRightUp()
            elif event.type==pygame.MOUSEWHEEL:
                bgEle=None
                for bgElement in Game.imageLayer.bgImages:
                    if bgElement.scaleRect.collidepoint(pygame.mouse.get_pos()):
                        bgEle=bgElement
                        break
                if bgEle!=None:
                    bgEle.scale+=event.y*0.1

            elif event.type==pygame.MOUSEMOTION:
                if dragging:
                    if Game.imageLayer.dragElement!=None:
                        mouse_x,mouse_y=event.pos
                        Game.imageLayer.dragElement.scaleRect.x=mouse_x+offset_x
                        Game.imageLayer.dragElement.scaleRect.y=mouse_y+offset_y
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
                elif event.key==pygame.K_BACKSLASH:
                    print("yes / is pressed")
                    if Game.isConsoling==False:
                        Game.startConsole()



                elif event.key==pygame.K_k:
                    print("yes,k is pressed")
                    Game.save()
                elif event.key==pygame.K_l:
                    Game.load()
                elif event.key==pygame.K_o:
                    print("o is pressed")
                    loadBgElement()

            elif event.type==pygame.KEYUP:
                if event.key == pygame.K_RIGHT or \
                        event.key == pygame.K_LEFT or \
                        event.key == pygame.K_UP or \
                        event.key == pygame.K_DOWN:
                    Game.player.animator.state=PersonState.quiet

        Game.isHover()
        pygame.display.flip()
        clock.tick(60)
    Game.stop()
    pygame.quit()


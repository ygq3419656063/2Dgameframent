
import sys
import threading
from queue import Queue
import pygame

command_queue = Queue()


class GameConsole(threading.Thread):
    def __init__(self,screen):
        super().__init__()
        self.running = True
        self.screen=screen

    def run(self):
        while self.running:
            try:
                cmd = input(">>> ")
                command_queue.put(cmd)
                self.handle_commands(self.screen)
            except EOFError:
                break

    def stop(self):
        self.running = False

    def handle_commands(self,screen):
        while not command_queue.empty():
            cmd = command_queue.get()
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

                    self.screen = pygame.display.set_mode(
                        (new_width, new_height),
                        pygame.RESIZABLE
                    )
                    print(f"窗口尺寸已调整为 {new_width}x{new_height}")
                except ValueError:
                    print("无效的尺寸参数！必须为整数")

            elif command == "exit":
                self.running = False
            else:
                print(f"未知命令：{command}")




class Game:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Game Console Demo")
        self.clock = pygame.time.Clock()
        self.running = True
        self.bg_color = (30, 30, 30)

        self.console = GameConsole(self.screen)
        self.console.start()

    def handle_commands(self):
        while not command_queue.empty():
            cmd = command_queue.get()
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

                    self.screen = pygame.display.set_mode(
                        (new_width, new_height),
                        pygame.RESIZABLE
                    )
                    print(f"窗口尺寸已调整为 {new_width}x{new_height}")
                except ValueError:
                    print("无效的尺寸参数！必须为整数")

            elif command == "exit":
                self.running = False
            else:
                print(f"未知命令：{command}")
    def run(self):
        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                #self.handle_commands()

                self.screen.fill(self.bg_color)
                pygame.display.flip()
                self.clock.tick(60)
        finally:
            # 确保资源清理
            #self.console.stop()
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()


import threading

class GameConsole(threading.Thread):
    def __init__(self,queue,game):
        super().__init__()
        self.running = True
        self.queue=queue
        self.game=game
        self.game.queue=queue
        self.game.gameConsole=self
        self.game.consoleQueue=queue

    def run(self):
        while self.running:
            try:
                cmd = input(">>> ")
                self.queue.put(cmd)
            except EOFError:
                break

    def stop(self):
        self.running = False

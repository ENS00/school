from draw import Game

class Gameloop(Game):
    def __init__(self):
        super().__init__()
        self.drawField()
        self.statusLights=0
        self.loop()

if __name__ == "__main__":
    game=Gameloop()
    game.tk.mainloop()
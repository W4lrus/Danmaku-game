from tkinter import *
from tkinter import ttk
from random import *

"""
TODO: grid instead of pack()
"""


class Game:
    def __init__(self):
        self.root = Tk()
        self.frame = Frame()
        self.frame.pack()        
        #App Keybindings, not game keybindings
        self.root.bind_all("<F1>", self.show_help)
        #Create all the widgets, setup the game
        self.create_widgets()
        #Start the programm, wait for the user to press start
        self.root.mainloop()

    def create_widgets(self):
        """Sets up all the widgets and textures"""
        #Python3 ttk styles
        style = ttk.Style()
        style.configure("Black.TButton", foreground = "black", background = "white")
        style.configure("Red.TButton", foreground = "red", background = "white")

        #Hello button
        self.hi_there = ttk.Button(self.frame, text="START",
                                style="Black.TButton", command=self.Start_game)
        self.hi_there.pack(side="top")
        #Quit Button
        self.quit = ttk.Button(self.frame, text="QUIT",
                            style="Red.TButton", command=self.root.destroy)
        self.quit.pack(side="bottom")

        #Game board
        self.game_board = Canvas(self.frame, width=700, height=500)

        #Images
        self.background = PhotoImage(file="skybiggergif.gif")    #background
        #place them on canvas
        self.game_board.create_image(300, 200, image=self.background)
        
        #Mark the canvas
        self.game_board.create_line(0, 2, 700, 2, fill="red")
        self.game_board.create_line(700, 2, 700, 500, fill="red")
        self.game_board.create_line(700, 500, 2, 500, fill="red")
        self.game_board.create_line(2, 500, 2, 2, fill="red")
        self.game_board.pack(side="bottom")

    def Start_game(self):
        print("Game started")
        #Textures
        self.planeimg = PhotoImage(file="plane.gif")   #plane
        self.coinimg = PhotoImage(file="gamecoin.gif")
        self.plane = self.game_board.create_image(100, 220, image=self.planeimg)

        self.coin_pos = randint(35, 465)
        self.coin = self.game_board.create_image(675, self.coin_pos, image = self.coinimg)
        
        #Game keybindings
        self.root.bind_all("<Key>", self.key_pressed)
        self.root.bind_all("<KeyRelease>", self.key_released)

        self.movement = 0
        self.Update_game()

    def Update_game(self):
        #TODO: Update positions, check collisions etc.
        """
        check position, plane must stay in canvas (700 px * 500 px), on screen
        plane size 130 px * 71 px
        TODO: create rectangle - hitbox for plane 
        """
        plane_coords = []
        plane_coords = self.game_board.coords(self.plane)
        if(plane_coords[1] > 460 and self.movement == 10):
            self.movement = 0
        if(plane_coords[1] < 40 and self.movement == -10):
            self.movement = 0
        
        #Spawn coins randomly, 35 px * 35 px
        """
        self.coins = []
        spawn_coin = randint(0, 25)
        if(spawn_coin == 1):
            self.coin_pos = randint(35, 465)
            self.coins.append(self.game_board.create_image(675, self.coin_pos, image = self.coin))
        #Move coins
        for x in self.coins:
            self.game_board.move(self.coin, -20, 0)
        """
        self.game_board.move(self.coin, -10, 0)
        self.game_board.move(self.plane, 0, self.movement)
        self.root.after(25, self.Update_game)

    """
    All the app events
    """

    def key_pressed(self, event):
        if(event.keysym == "Up"):
            self.movement = -10
        elif(event.keysym == "Down"):
            self.movement = 10

    def key_released(self, event):
        self.movement = 0
            

    def show_help(self, event):
        print("Looks like you need some help pal.")

app = Game()

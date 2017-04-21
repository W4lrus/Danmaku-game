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
        
        #Points label
         
        self.label_points = Label(self.frame, text="0")
        self.label_points.pack(side="bottom")

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
        #TODO: Download img
        #self.enemyimg = PhotoImage(file="enemy.gif")
        
        """
        self.coin_pos = randint(35, 465)
        self.coin = self.game_board.create_image(675, self.coin_pos, image = self.coinimg)
        """
        self.coins = []
        self.enemies = []
        self.points = 0

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
        spawn_coin = randint(0, 25)
               #Move coins
        for x in self.coins:
            self.game_board.move(self.coin, -20, 0)
        
        self.coins.append(self.coin)
        self.game_board.move(self.coins[0], -10, 0)
        """
        self.create_coins()
        #Spawn enemies
        #self.create_enemies()

        self.game_board.move(self.plane, 0, self.movement)
        self.root.after(25, self.Update_game)

    def create_coins(self):
        """Spawn, move coins and check collision with plane"""
        #Create coins randomly
        spawn_coin = randint(0, 25)
        if(spawn_coin == 1):
            self.coin_pos = randint(35, 465)
            self.cn = self.game_board.create_image(675, self.coin_pos, image = self.coinimg)
            self.coins.append(self.cn)
        #move all coins

        plane_coords = []
        plane_coords = self.game_board.coords(self.plane)


        for x in self.coins:
            #self.game_board.move(x, -8, 0)
            coin_coords = []
            coin_coords = self.game_board.coords(x)
            coin_coords[0] -= 8
            self.game_board.coords(x, coin_coords[0], coin_coords[1])
            coin_coords = self.game_board.coords(x)
            
            #check collision, plane(130*71) position on x axis is 80 to 150
           
            if(coin_coords[0] < 150 and coin_coords[0] > 80):
                if(coin_coords[1] > plane_coords[1]-40 and coin_coords[1] < plane_coords[1]+40):
                    #Delete coin and add points
                    """
                    self.coins.remove(x)
                    x.destroy()
                    """
                    #one coin = 18 points 
                    self.points += 1
                    self.label_points.config(text=str(self.points))
                    print("Collision")
                    self.game_board.delete(x)
                    self.coins.remove(x)
                
    """       
    def create_enemies(self):
        #Spawns enemy planes, if you hit them you lose points
        spawn_enemy = randint(0, 50)
        if(spawn_enemy == 1):
            #Spawn enemy plane
            
            plane_coords = []
            plane_coords = self.game_board.coords(self.plane)

            enemy_pos = randint(45, 455)
            self.enemy = self.game_board.create_image(650, enemy_pos, image="self.enemyimg")
            self.enemies.append(self.enemy)

        #move enemy planes 
        for b in self.enemies:
            enemy_coords = []
            enemy_coords = self.game_board.coords(b)
            enemy_coords[0] -= 8
            self.game_board.coords(b, enemy_coords[0], enemy_coords[1])
            enemy_coords = self.game_board.coords(b)

            #check collision
            if(enemy_coords[0] < 150 and coin_coords[0] > 80):
                if(coin_coords[1] > plane_coords[1]-40 and coin_coords[1] < plane_coords[1]+40):
                    #Delete enemy plane and lose points
                    self.points -= 1
                    self.label_points.config(text=str(self.points))
                    print("Collision")
                    self.game_board.delete(b)
                    self.enemies.remove(b)




    """       

        
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

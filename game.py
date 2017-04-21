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
        self.game_board = Canvas(self.frame, width=870, height=621)

        #Images
        self.background = PhotoImage(file="skybiggergif.gif")    #background
        #place them on canvas
        self.game_board.create_image(435, 310, image=self.background)

        self.game_board.pack(side="bottom")

    def Start_game(self):
        print("Game started")
        #Textures
        self.planeimg = PhotoImage(file="plane.gif")   #plane
        self.coinimg = PhotoImage(file="gamecoin.gif")
        self.plane = self.game_board.create_image(100, 220, image=self.planeimg)
        self.enemyimg = PhotoImage(file="enemyplane.gif")
        
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
        check position, plane must stay in canvas (870 px * 621 px), on screen
        plane size 130 px * 71 px
        """
        plane_coords = []
        plane_coords = self.game_board.coords(self.plane)
        if(plane_coords[1] > 589 and self.movement == 10):
            self.movement = 0
        if(plane_coords[1] < 40 and self.movement == -10):
            self.movement = 0
        
        #Spawn coins randomly
        self.create_coins()
        #Spawn enemies
        self.create_enemies()

        self.game_board.move(self.plane, 0, self.movement)
        self.root.after(25, self.Update_game)

    def create_coins(self):
        """Spawn, move coins and check collision with plane"""
        #Create coins randomly
        spawn_coin = randint(0, 50)
        if(spawn_coin == 1):
            self.coin_pos = randint(35, 686)
            self.cn = self.game_board.create_image(845, self.coin_pos, image = self.coinimg)
            self.coins.append(self.cn)
        #get player plane coordinates    
        plane_coords = []
        plane_coords = self.game_board.coords(self.plane)

        #move all coins
        for x in self.coins:
            coin_coords = []
            coin_coords = self.game_board.coords(x)
            coin_coords[0] -= 8
            self.game_board.coords(x, coin_coords[0], coin_coords[1])
            coin_coords = self.game_board.coords(x)
            
            #check collision, plane(130*71) position on x axis is 80 to 150
           
            if(coin_coords[0] < 150 and coin_coords[0] > 80):
                if(coin_coords[1] > plane_coords[1]-40 and coin_coords[1] < plane_coords[1]+40):
                    #Delete coin and add points
                    self.points += 1
                    self.label_points.config(text=str(self.points))
                    self.game_board.delete(x)
                    self.coins.remove(x)
                  
    def create_enemies(self):
        #get player plane coordinates
        plane_coords = []
        plane_coords = self.game_board.coords(self.plane)
        
        #Spawns enemy planes, if you hit them you lose points
        spawn_enemy = randint(0, 20)
        if(spawn_enemy == 1):          
            #Spawn enemy plane randomly
            enemy_pos = randint(45, 676)
            self.enemy = self.game_board.create_image(840, enemy_pos, image=self.enemyimg)
            self.enemies.append(self.enemy)

        #move enemy planes 
        for b in self.enemies:
            enemy_coords = []
            enemy_coords = self.game_board.coords(b)
            enemy_coords[0] -= 8
            self.game_board.coords(b, enemy_coords[0], enemy_coords[1])
            enemy_coords = self.game_board.coords(b)

            #check collision
            if(enemy_coords[0] < 150 and enemy_coords[0] > 80):
                if(enemy_coords[1] > plane_coords[1]-45 and enemy_coords[1] < plane_coords[1]+45):
                    #Delete enemy plane and lose points
                    self.points -= 1
                    #You lose if you get hit too much
                    if(self.points < 0):
                        print("Game over!")
                        self.game_over()
                    self.label_points.config(text=str(self.points))
                    print("Collision!")
                    self.game_board.delete(b)
                    self.enemies.remove(b)
                    
    def game_over(self):
        self.game_board.delete("all")
        self.game_board.create_image(435, 310, image=self.background)
        self.root.mainloop()
        
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
